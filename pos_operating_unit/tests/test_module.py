from odoo import fields
from odoo.exceptions import AccessError
from odoo.tests.common import TransactionCase


class TestModule(TransactionCase):
    def setUp(self):
        super(TestModule, self).setUp()
        self.ResUsers = self.env["res.users"]
        self.PosOrder = self.env["pos.order"]
        self.pos_product = self.env.ref("point_of_sale.whiteboard_pen")
        self.pricelist = self.env.ref("product.list0")

        # Create a new pos config and open it
        self.pos_config = self.env.ref("point_of_sale.pos_config_main").copy()

        # company
        self.company = self.env.ref("base.main_company")
        # group
        self.group_user = self.env.ref("base.group_user")
        self.group_pos_manager = self.env.ref("point_of_sale.group_pos_manager")
        # Main Operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2B Operating Unit
        self.b2b = self.env.ref("operating_unit.b2b_operating_unit")

        self.pos_config.operating_unit_ids = [(6, 0, [self.ou1.id])]
        self.pos_config.open_session_cb()

        # Create users
        self.user1_id = self._create_user(
            "user_1",
            [self.group_user, self.group_pos_manager],
            self.company,
            [self.ou1, self.b2b],
        )
        self.user2_id = self._create_user(
            "user_2",
            [self.group_user, self.group_pos_manager],
            self.company,
            [self.b2b],
        )

    def test_operating_unit_access_config(self):
        config1_ids = self.env["pos.config"].with_user(self.user1_id).search([])
        self.assertIn(self.pos_config, config1_ids)
        config2_ids = self.env["pos.config"].with_user(self.user2_id).search([])
        self.assertNotIn(self.pos_config, config2_ids)

    def test_operating_unit_access_session(self):
        self.pos_config.current_session_id.with_user(self.user1_id).read()
        with self.assertRaises(AccessError):
            self.pos_config.current_session_id.with_user(self.user2_id).read()

    def test_operating_unit_access_order_and_line_and_payment(self):
        order = self._create_order()
        order.with_user(self.user1_id).read()
        order.lines.with_user(self.user1_id).read()
        with self.assertRaises(AccessError):
            order.with_user(self.user2_id).read()
        with self.assertRaises(AccessError):
            order.lines.with_user(self.user2_id).read()
        order.payment_ids.with_user(self.user1_id).read()
        with self.assertRaises(AccessError):
            order.payment_ids.with_user(self.user2_id).read()

    def _create_order(self):
        # Create order
        account_id = self.env.user.partner_id.property_account_receivable_id.id
        order_data = {
            "id": "0006-001-0010",
            "to_invoice": False,
            "data": {
                "pricelist_id": self.pricelist.id,
                "user_id": 1,
                "name": "Order 0006-001-0010",
                "partner_id": False,
                "amount_paid": 1000,
                "pos_session_id": self.pos_config.current_session_id.id,
                "lines": [
                    [
                        0,
                        0,
                        {
                            "product_id": self.pos_product.id,
                            "qty": 1,
                            "price_subtotal": 1000,
                            "price_subtotal_incl": 1000,
                        },
                    ]
                ],
                "statement_ids": [
                    [
                        0,
                        0,
                        {
                            "payment_method_id": self.pos_config.payment_method_ids[
                                0
                            ].id,
                            "amount": 1000,
                            "name": fields.Datetime.now(),
                            "account_id": account_id,
                            "session_id": self.pos_config.current_session_id.id,
                        },
                    ]
                ],
                "creation_date": "2022-11-27 15:51:03",
                "amount_tax": 0,
                "fiscal_position_id": False,
                "uid": "00001-001-0001",
                "amount_return": 0,
                "sequence_number": 1,
                "amount_total": 1000.0,
                "session_id": self.pos_config.current_session_id.id,
            },
        }
        result = self.PosOrder.create_from_ui([order_data])
        order = self.PosOrder.browse(result[0].get("id"))
        return order

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.ResUsers.with_context({"no_reset_password": True}).create(
            {
                "name": "Chicago Purchase User",
                "login": login,
                "password": "demo",
                "email": "chicago@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user.id
