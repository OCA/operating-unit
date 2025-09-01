# Copyright 2024 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import fields
from odoo.exceptions import AccessError
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


@tagged("post_install", "-at_install")
class TestPOSOperatingUnit(OperatingUnitCommon):
    """Test Point of Sale Operating Unit access controls and functionality."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Setup models
        cls.PosOrder = cls.env["pos.order"]
        cls.PosConfig = cls.env["pos.config"]
        cls.PosSession = cls.env["pos.session"]

        # Setup product for testing
        cls.pos_product = cls.env["product.product"].create(
            {
                "name": "Test POS Product",
                "available_in_pos": True,
                "list_price": 1000.0,
            }
        )

        # Setup pricelist
        cls.pricelist = cls.env["product.pricelist"].create(
            {
                "name": "Test POS Pricelist",
                "currency_id": cls.env.company.currency_id.id,
            }
        )

        # Setup groups
        cls.group_pos_manager = cls.env.ref("point_of_sale.group_pos_manager")
        cls.group_account_invoice = cls.env.ref("account.group_account_invoice")

        # Create POS config with operating unit
        cls.pos_config = cls.env["pos.config"].create(
            {
                "name": "Test POS Config",
                "operating_unit_ids": [Command.set([cls.ou1.id])],
                "available_pricelist_ids": [Command.set([cls.pricelist.id])],
                "pricelist_id": cls.pricelist.id,
            }
        )

        # Open session
        cls.pos_config.open_ui()

        # Configure users with proper groups and operating units
        cls.user1.write(
            {
                "groups_id": [
                    Command.link(cls.group_pos_manager.id),
                    Command.link(cls.group_account_invoice.id),
                ],
                "operating_unit_ids": [Command.link(cls.ou1.id)],
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
        """Test that users can only access POS configs for their operating units."""
        # User1 has access to ou1 (same as pos_config)
        config1_ids = self.PosConfig.with_user(self.user1).search([])
        self.assertIn(self.pos_config, config1_ids)

        # User2 has access to b2b (different from pos_config)
        config2_ids = self.PosConfig.with_user(self.user2).search([])
        self.assertNotIn(self.pos_config, config2_ids)

    def test_operating_unit_access_session(self):
        """Test that users can only access sessions for their operating units."""
        # User1 should be able to read the session
        self.pos_config.current_session_id.with_user(self.user1).read()

        # User2 should not have access
        with self.assertRaises(AccessError):
            self.pos_config.current_session_id.with_user(self.user2).read()

    def test_operating_unit_access_order_and_line_and_payment(self):
        """Test that users can only access orders for their operating units."""
        order = self._create_order()

        # User1 should have access to order and related records
        order.with_user(self.user1).read()
        order.lines.with_user(self.user1).read()
        order.payment_ids.with_user(self.user1).read()

        # User2 should not have access
        with self.assertRaises(AccessError):
            order.with_user(self.user2).read()
        with self.assertRaises(AccessError):
            order.lines.with_user(self.user2).read()
        with self.assertRaises(AccessError):
            order.payment_ids.with_user(self.user2).read()

    def _create_order(self):
        """Create a test POS order using the modern Odoo 18 approach."""
        # Create order using sync_from_ui method
        order_data = {
            "id": "0006-001-0010",
            "to_invoice": False,
            "session_id": self.pos_config.current_session_id.id,
            "date_order": fields.Datetime.to_string(fields.Datetime.now()),
            "pricelist_id": self.pricelist.id,
            "user_id": self.env.user.id,
            "name": "Order 0006-001-0010",
            "partner_id": False,
            "amount_paid": 1000.0,
            "amount_total": 1000.0,
            "amount_tax": 0.0,
            "amount_return": 0.0,
            "fiscal_position_id": False,
            "sequence_number": 1,
            "uuid": "00001-001-0001",
            "lines": [
                [
                    0,
                    0,
                    {
                        "product_id": self.pos_product.id,
                        "qty": 1.0,
                        "price_unit": 1000.0,
                        "price_subtotal": 1000.0,
                        "price_subtotal_incl": 1000.0,
                        "discount": 0.0,
                    },
                ]
            ],
            "payment_ids": [
                [
                    0,
                    0,
                    {
                        "payment_method_id": self.pos_config.payment_method_ids[0].id,
                        "amount": 1000.0,
                    },
                ]
            ],
        }

        # Create the order
        result = self.PosOrder.sync_from_ui([order_data])
        if not result or "pos.order" not in result:
            raise ValueError("Failed to create POS order")

        # Get order data from result
        pos_orders = result["pos.order"]
        if not pos_orders:
            raise ValueError("No order data in result")

        # Extract order ID from the first order data
        order_data_dict = pos_orders[0] if pos_orders else {}
        order_id = order_data_dict.get("id")

        if not order_id:
            raise ValueError("Failed to get order ID from result")

        return self.PosOrder.browse(order_id)
