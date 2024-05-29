# © 2019 ForgeFlow S.L. -
# Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.models import Command

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestSaleOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.sale_model = cls.env["sale.order"]
        cls.sale_line_model = cls.env["sale.order.line"]
        cls.sale_team_model = cls.env["crm.team"]
        cls.acc_move_model = cls.env["account.move"]
        cls.product_model = cls.env["product.product"]
        cls.payment_model = cls.env["sale.advance.payment.inv"]
        # Company
        cls.grp_sale_user = cls.env.ref("sales_team.group_sale_manager")
        cls.grp_acc_user = cls.env.ref("account.group_account_invoice")
        # Payment Term
        cls.pay = cls.env.ref("account.account_payment_term_immediate")
        # Customer
        cls.customer = cls.env.ref("base.res_partner_2")
        # Price list
        cls.pricelist = cls.env["product.pricelist"].search([], limit=1)
        # Products
        cls.product1 = cls.env.ref("product.product_product_2")
        cls.product1.write({"invoice_policy": "order"})
        # Update users
        cls.user1.write(
            {
                "groups_id": [
                    Command.link(cls.grp_sale_user.id),
                    Command.link(cls.grp_acc_user.id),
                ],
                "operating_unit_ids": [
                    Command.link(cls.ou1.id),
                    Command.link(cls.b2c.id),
                ],
            }
        )
        cls.user2.write(
            {
                "groups_id": [
                    Command.link(cls.grp_sale_user.id),
                    Command.link(cls.grp_acc_user.id),
                ],
                "default_operating_unit_id": [],
            }
        )

        # Create sales team OU1
        cls.sale_team_ou1 = cls._create_sale_team(cls.user1.id, cls.ou1)

        # Create sales team OU2
        cls.sale_team_b2c = cls._create_sale_team(cls.user2.id, cls.b2c)

        # Create Sale Order1
        cls.sale1 = cls._create_sale_order(
            cls.user1.id,
            cls.customer,
            cls.product1,
            cls.pricelist,
            cls.sale_team_ou1,
        )
        # Create Sale Order2
        cls.sale2 = cls._create_sale_order(
            cls.user2.id,
            cls.customer,
            cls.product1,
            cls.pricelist,
            cls.sale_team_b2c,
        )

    @classmethod
    def _create_sale_team(cls, uid, operating_unit):
        """Create a sale team."""
        team = (
            cls.sale_team_model.with_user(uid)
            .with_context(mail_create_nosubscribe=True)
            .create(
                {"name": operating_unit.name, "operating_unit_id": operating_unit.id}
            )
        )
        return team

    @classmethod
    def _create_sale_order(cls, uid, customer, product, pricelist, team):
        """Create a sale order."""
        sale = cls.sale_model.with_user(uid).create(
            {
                "partner_id": customer.id,
                "partner_invoice_id": customer.id,
                "partner_shipping_id": customer.id,
                "pricelist_id": pricelist.id,
                "team_id": team.id,
                "operating_unit_id": team.operating_unit_id.id,
            }
        )
        cls.sale_line_model.with_user(uid).create(
            {
                "order_id": sale.id,
                "product_id": product.id,
                "name": "Sale Order Line",
                "product_uom_qty": 1,
            }
        )
        return sale

    def _confirm_sale(self, sale):
        sale.action_confirm()
        sale_context = {
            "active_model": "sale.order",
            "active_ids": [sale.id],
            "active_id": sale.id,
        }
        # Let's do an invoice with invoiceable lines
        payment = (
            self.env["sale.advance.payment.inv"]
            .with_context(**sale_context)
            .create({"advance_payment_method": "delivered"})
        )
        res = payment.create_invoices()
        invoice_id = res["res_id"]
        return invoice_id

    def test_security(self):
        """Test Sale Operating Unit"""
        # User 2 is only assigned to Operating Unit B2C, and cannot
        # Access Sales order from Main Operating Unit.
        sale = self.sale_model.with_user(self.user2.id).search(
            [("id", "=", self.sale1.id), ("operating_unit_id", "=", self.ou1.id)]
        )
        self.assertEqual(
            sale.ids, [], "User 2 should not have access to " "OU %s" % self.ou1.name
        )
        # Confirm Sale1
        self._confirm_sale(self.sale1)
        # Confirm Sale2
        b2c_invoice_id = self._confirm_sale(self.sale2)
        # Checks that invoice has OU b2c
        b2c = self.acc_move_model.with_user(self.user2.id).search(
            [("id", "=", b2c_invoice_id), ("operating_unit_id", "=", self.b2c.id)]
        )
        self.assertNotEqual(b2c.ids, [], "Invoice should have b2c OU")

    def test_security_2(self):
        """Test Sale Operating Unit"""
        # User 2 is only assigned to Operating Unit B2C, and cannot
        # Access Sales order from Main Operating Unit.
        sale = self.sale_model.with_user(self.user2.id).search(
            [("id", "=", self.sale1.id), ("operating_unit_id", "=", self.ou1.id)]
        )
        self.assertEqual(
            sale.ids, [], "User 2 should not have access to " "OU %s" % self.ou1.name
        )

        sale = self.sale_model.with_user(self.user2.id).search(
            [("id", "=", self.sale2.id), ("operating_unit_id", "=", self.b2c.id)]
        )

        self.assertEqual(
            len(sale.ids), 1, "User 1 should have access to " "OU %s" % self.b2c.name
        )
