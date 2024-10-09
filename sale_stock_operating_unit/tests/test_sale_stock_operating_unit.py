# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import common


class TestSaleStockOperatingUnit(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.res_groups = cls.env["res.groups"]
        cls.res_users_model = cls.env["res.users"]
        cls.warehouse_model = cls.env["stock.warehouse"]
        cls.sale_model = cls.env["sale.order"]
        cls.sale_line_model = cls.env["sale.order.line"]
        cls.sale_team_model = cls.env["crm.team"]
        # Company
        cls.company = cls.env.ref("base.main_company")
        # Groups
        cls.grp_sale_user = cls.env.ref("sales_team.group_sale_manager")
        cls.grp_acc_user = cls.env.ref("account.group_account_invoice")
        # Main Operating Unit
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        cls.b2c = cls.env.ref("operating_unit.b2c_operating_unit")
        # Customer
        cls.customer = cls.env.ref("base.res_partner_2")
        # Price list
        cls.pricelist = cls.env.ref("product.list0")
        # Products
        cls.product1 = cls.env.ref("product.product_product_7")
        cls.product1.write({"invoice_policy": "order"})
        # Create user1
        cls.user1 = cls._create_user(
            "user_1",
            [cls.grp_sale_user, cls.grp_acc_user],
            cls.company,
            [cls.ou1, cls.b2c],
        )
        # Create user2
        cls.user2 = cls._create_user(
            "user_2", [cls.grp_sale_user, cls.grp_acc_user], cls.company, [cls.b2c]
        )

        # Create sales team OU1
        cls.sale_team_ou1 = cls._create_sale_team(cls.user1.id, cls.ou1)

        # Create sales team OU2
        cls.sale_team_b2c = cls._create_sale_team(cls.user2.id, cls.b2c)

        # Warehouses
        cls.ou1_wh = cls.env.ref("stock.warehouse0")
        cls.b2c_wh = cls.env.ref("stock_operating_unit.stock_warehouse_b2c")
        # Locations
        cls.b2c_wh.lot_stock_id.write(
            {"company_id": cls.company.id, "operating_unit_id": cls.b2c.id}
        )

        # Create Sale Order1
        cls.sale1 = cls._create_sale_order(
            cls.user1.id,
            cls.customer,
            cls.product1,
            cls.pricelist,
            cls.sale_team_ou1,
            cls.ou1_wh,
        )
        # Create Sale Order2
        cls.sale2 = cls._create_sale_order(
            cls.user2.id,
            cls.customer,
            cls.product1,
            cls.pricelist,
            cls.sale_team_b2c,
            cls.b2c_wh,
        )

    @classmethod
    def _create_user(cls, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = cls.res_users_model.create(
            {
                "name": "Test Sales User",
                "login": login,
                "password": "demo",
                "email": "example@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user

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
    def _create_sale_order(cls, uid, customer, product, pricelist, team, wh):
        """Create a sale order."""
        sale = cls.sale_model.with_user(uid).create(
            {
                "partner_id": customer.id,
                "partner_invoice_id": customer.id,
                "partner_shipping_id": customer.id,
                "pricelist_id": pricelist.id,
                "team_id": team.id,
                "operating_unit_id": team.operating_unit_id.id,
                "warehouse_id": wh.id,
            }
        )
        cls.sale_line_model.with_user(uid).create(
            {"order_id": sale.id, "product_id": product.id, "name": "Sale Order Line"}
        )
        return sale

    @classmethod
    def _confirm_sale(cls, sale):
        sale.action_confirm()
        return True

    def test_security(self):
        """Test Sale Operating Unit"""
        # Confirm Sale1
        self._confirm_sale(self.sale1)
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(
            self.sale1.operating_unit_id,
            self.sale1.picking_ids.operating_unit_id,
            "OU in Sale Order and Picking should be same",
        )
        # Confirm Sale2
        self._confirm_sale(self.sale2)
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(
            self.sale2.operating_unit_id,
            self.sale2.picking_ids.operating_unit_id,
            "OU in Sale Order and Picking should be same",
        )
