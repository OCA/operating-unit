# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestAccountOperatingUnit(AccountTestInvoicingCommon):
    def setUp(self):
        super().setUp()
        self.res_users_model = self.env["res.users"]
        self.aml_model = self.env["account.move.line"]
        self.move_model = self.env["account.move"]
        self.account_model = self.env["account.account"]
        self.journal_model = self.env["account.journal"]
        self.product_model = self.env["product.product"]
        self.payment_model = self.env["account.payment"]
        self.register_payments_model = self.env["account.payment.register"]

        # company
        self.company = self.env.user.company_id
        self.grp_acc_manager = self.env.ref("account.group_account_manager")
        # Main Operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2B Operating Unit
        self.b2b = self.env.ref("operating_unit.b2b_operating_unit")
        # B2C Operating Unit
        self.b2c = self.env.ref("operating_unit.b2c_operating_unit")
        # Assign user to main company to allow to write OU
        self.env.user.write(
            {
                "company_ids": [(4, self.env.ref("base.main_company").id)],
                "operating_unit_ids": [
                    (4, self.b2b.id),
                    (4, self.b2c.id),
                ],
            }
        )
        # Assign company to OU
        (self.ou1 + self.b2b + self.b2c).write({"company_id": self.company.id})
        # Partner
        self.partner1 = self.env.ref("base.res_partner_1")
        # Products
        self.product1 = self.env.ref("product.product_product_7")
        self.product2 = self.env.ref("product.product_product_9")
        self.product3 = self.env.ref("product.product_product_11")

        # Payment methods
        self.payment_method_manual_in = self.env.ref(
            "account.account_payment_method_manual_in"
        )

        # Create user1
        self.user_id = self.res_users_model.with_context(no_reset_password=True).create(
            {
                "name": "Test Account User",
                "login": "user_1",
                "password": "demo",
                "email": "example@yourcompany.com",
                "company_id": self.company.id,
                "company_ids": [(4, self.company.id)],
                "operating_unit_ids": [(4, self.b2b.id), (4, self.b2c.id)],
                "groups_id": [(6, 0, [self.grp_acc_manager.id])],
            }
        )
        # Create cash - test account
        user_type = self.env.ref("account.data_account_type_current_assets")
        self.current_asset_account_id = self.account_model.create(
            {
                "name": "Current asset - Test",
                "code": "test_current_asset",
                "user_type_id": user_type.id,
                "company_id": self.company.id,
            }
        )
        # Create Inter-OU Clearing - test account
        user_type = self.env.ref("account.data_account_type_equity")
        self.inter_ou_account_id = self.account_model.create(
            {
                "name": "Inter-OU Clearing",
                "code": "test_inter_ou",
                "user_type_id": user_type.id,
                "company_id": self.company.id,
            }
        )
        # Assign the Inter-OU Clearing account to the company
        self.company.inter_ou_clearing_account_id = self.inter_ou_account_id.id
        self.company.ou_is_self_balanced = True

        # Create user2
        self.user2_id = self.res_users_model.with_context(
            no_reset_password=True
        ).create(
            {
                "name": "Test Account User",
                "login": "user_2",
                "password": "demo",
                "email": "example@yourcompany.com",
                "company_id": self.company.id,
                "company_ids": [(4, self.company.id)],
                "operating_unit_ids": [(4, self.b2c.id)],
                "groups_id": [(6, 0, [self.grp_acc_manager.id])],
            }
        )

        # Create a cash account 1
        user_type = self.env.ref("account.data_account_type_liquidity")
        self.cash1_account_id = self.account_model.create(
            {
                "name": "Cash 1 - Test",
                "code": "test_cash_1",
                "user_type_id": user_type.id,
                "company_id": self.company.id,
            }
        )

        # Create a journal for cash account 1, associated to the main
        # operating unit
        self.cash_journal_ou1 = self.journal_model.create(
            {
                "name": "Cash Journal 1 - Test",
                "code": "cash1",
                "type": "cash",
                "company_id": self.company.id,
                "default_account_id": self.cash1_account_id.id,
                "operating_unit_id": self.ou1.id,
            }
        )
        # Create a cash account 2
        user_type = self.env.ref("account.data_account_type_liquidity")
        self.cash2_account_id = self.account_model.create(
            {
                "name": "Cash 2 - Test",
                "code": "cash2",
                "user_type_id": user_type.id,
                "company_id": self.company.id,
            }
        )

        # Create a journal for cash account 2, associated to the operating
        # unit B2B
        self.cash2_journal_b2b = self.journal_model.create(
            {
                "name": "Cash Journal 2 - Test",
                "code": "test_cash_2",
                "type": "cash",
                "company_id": self.company.id,
                "default_account_id": self.cash2_account_id.id,
                "operating_unit_id": self.b2b.id,
            }
        )

    def _prepare_invoice(self, operating_unit_id, name="Test Supplier Invoice"):
        line_products = [
            (self.product1, 1000),
            (self.product2, 500),
            (self.product3, 800),
        ]
        # Prepare invoice lines
        lines = []
        acc_type = self.env.ref("account.data_account_type_expenses")
        for product, qty in line_products:
            line_values = {
                "name": product.name,
                "product_id": product.id,
                "quantity": qty,
                "price_unit": 50,
                "account_id": self.env["account.account"]
                .search([("user_type_id", "=", acc_type.id)], limit=1)
                .id,
            }
            lines.append((0, 0, line_values))
        inv_vals = {
            "partner_id": self.partner1.id,
            "operating_unit_id": operating_unit_id,
            "name": name,
            "move_type": "in_invoice",
            "invoice_line_ids": lines,
        }
        return inv_vals
