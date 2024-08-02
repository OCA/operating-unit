# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.models import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


@tagged("post_install", "-at_install")
class TestAccountOperatingUnit(AccountTestInvoicingCommon, OperatingUnitCommon):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.aml_model = cls.env["account.move.line"]
        cls.move_model = cls.env["account.move"]
        cls.account_model = cls.env["account.account"]
        cls.journal_model = cls.env["account.journal"]
        cls.product_model = cls.env["product.product"]
        cls.payment_model = cls.env["account.payment"]
        cls.register_payments_model = cls.env["account.payment.register"]

        # company
        cls.grp_acc_manager = cls.env.ref("account.group_account_manager")
        cls.grp_acc_config = cls.env.ref("account.group_account_user")
        # Main Operating Unit
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        # B2B Operating Unit
        cls.b2b = cls.env.ref("operating_unit.b2b_operating_unit")
        # B2C Operating Unit
        cls.b2c = cls.env.ref("operating_unit.b2c_operating_unit")
        # Assign user to main company to allow to write OU
        cls.env.user.write(
            {
                "operating_unit_ids": [
                    Command.link(cls.b2b.id),
                    Command.link(cls.b2c.id),
                ],
                "company_ids": [Command.link(cls.company.id)],
            }
        )
        # Products
        cls.product1 = cls.env.ref("product.product_product_7")
        cls.product2 = cls.env.ref("product.product_product_9")
        cls.product3 = cls.env.ref("product.product_product_11")

        # Payment methods
        cls.payment_method_manual_in = cls.env.ref(
            "account.account_payment_method_manual_in"
        )

        cls.user1.write(
            {
                "groups_id": [
                    Command.link(cls.grp_acc_manager.id),
                    Command.link(cls.grp_acc_config.id),
                ],
                "operating_unit_ids": [
                    Command.link(cls.b2b.id),
                    Command.link(cls.b2c.id),
                ],
            }
        )
        # Create cash - test account
        cls.current_asset_account_id = cls.account_model.create(
            {
                "name": "Current asset - Test",
                "code": "test.current.asset",
                "account_type": "asset_current",
                "company_id": cls.company.id,
            }
        )
        # Create Inter-OU Clearing - test account
        cls.inter_ou_account_id = cls.account_model.create(
            {
                "name": "Inter-OU Clearing",
                "code": "test.inter.ou",
                "account_type": "equity",
                "company_id": cls.company.id,
            }
        )
        # Assign the Inter-OU Clearing account to the company
        cls.company.inter_ou_clearing_account_id = cls.inter_ou_account_id.id
        cls.company.ou_is_self_balanced = True

        # Create user2
        cls.user2.write(
            {
                "groups_id": [
                    Command.link(cls.grp_acc_manager.id),
                    Command.link(cls.grp_acc_config.id),
                ],
                "operating_unit_ids": [
                    Command.link(cls.b2c.id),
                ],
            }
        )

        # Create a cash account 1
        cls.cash1_account_id = cls.account_model.create(
            {
                "name": "Cash 1 - Test",
                "code": "test.cash.1",
                "account_type": "asset_current",
                "company_id": cls.company.id,
            }
        )

        # Create a journal for cash account 1, associated to the main
        # operating unit
        cls.cash_journal_ou1 = cls.journal_model.create(
            {
                "name": "Cash Journal 1 - Test",
                "code": "cash1",
                "type": "cash",
                "company_id": cls.company.id,
                "default_account_id": cls.cash1_account_id.id,
                "operating_unit_id": cls.ou1.id,
            }
        )
        # Create a cash account 2
        cls.cash2_account_id = cls.account_model.create(
            {
                "name": "Cash 2 - Test",
                "code": "cash2",
                "account_type": "asset_current",
                "company_id": cls.company.id,
            }
        )

        # Create a journal for cash account 2, associated to the operating
        # unit B2B
        cls.cash2_journal_b2b = cls.journal_model.create(
            {
                "name": "Cash Journal 2 - Test",
                "code": "test_cash_2",
                "type": "cash",
                "company_id": cls.company.id,
                "default_account_id": cls.cash2_account_id.id,
                "operating_unit_id": cls.b2b.id,
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
        for product, qty in line_products:
            line_values = {
                "name": product.name,
                "product_id": product.id,
                "quantity": qty,
                "price_unit": 50,
                "account_id": self.env["account.account"]
                .search(
                    [
                        ("account_type", "=", "expense"),
                        ("company_id", "=", self.company.id),
                    ],
                    limit=1,
                )
                .id,
                # Adding this line so the taxes are explicitly excluded from the lines
                "tax_ids": [],
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
