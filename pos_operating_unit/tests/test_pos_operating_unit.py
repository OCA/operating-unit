from odoo import fields
from odoo.exceptions import AccessError
from odoo.models import Command

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestPOSOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.PosOrder = cls.env["pos.order"]
        cls.pos_product = cls.env.ref("point_of_sale.whiteboard_pen")
        cls.pricelist = cls.env["product.pricelist"].search([], limit=1)

        # Create a new pos config and open it
        cls.pos_config = cls.env.ref("point_of_sale.pos_config_main").copy()
        cls.group_pos_manager = cls.env.ref("point_of_sale.group_pos_manager")
        cls.group_account_invoice = cls.env.ref("account.group_account_invoice")

        cls.pos_config.operating_unit_ids = [Command.set([cls.ou1.id])]
        cls.pos_config.open_ui()

        cls.user1.write(
            {
                "groups_id": [
                    Command.link(cls.group_pos_manager.id),
                    Command.link(cls.group_account_invoice.id),
                ],
                "operating_unit_ids": [Command.link(cls.b2b.id)],
            }
        )
        cls.user2.write(
            {
                "groups_id": [
                    Command.link(cls.group_pos_manager.id),
                    Command.link(cls.group_account_invoice.id),
                ],
                "operating_unit_ids": [Command.set([cls.b2b.id])],
            }
        )

    def test_operating_unit_access_config(self):
        config1_ids = self.env["pos.config"].with_user(self.user1).search([])
        self.assertIn(self.pos_config, config1_ids)
        config2_ids = self.env["pos.config"].with_user(self.user2).search([])
        self.assertNotIn(self.pos_config, config2_ids)

    def test_operating_unit_access_session(self):
        self.pos_config.current_session_id.with_user(self.user1).read()
        with self.assertRaises(AccessError):
            self.pos_config.current_session_id.with_user(self.user2).read()

    def test_operating_unit_access_order_and_line_and_payment(self):
        order = self._create_order()
        order.with_user(self.user1).read()
        order.lines.with_user(self.user1).read()
        with self.assertRaises(AccessError):
            order.with_user(self.user2).read()
        with self.assertRaises(AccessError):
            order.lines.with_user(self.user2).read()
        order.payment_ids.with_user(self.user1).read()
        with self.assertRaises(AccessError):
            order.payment_ids.with_user(self.user2).read()

    def _create_order(self):
        # Create order
        account_id = self.env.user.partner_id.property_account_receivable_id.id
        order_data = {
            "id": "0006-001-0010",
            "to_invoice": False,
            "data": {
                "date_order": fields.Datetime.to_string(fields.Datetime.now()),
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
                            "price_unit": 1000,
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
