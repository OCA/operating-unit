# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.exceptions import UserError
from odoo.tests import Form

from odoo.addons.purchase_operating_unit.tests.test_purchase_operating_unit import (
    TestPurchaseOperatingUnit,
)


class TestPurchaseStockOperatingUnit(TestPurchaseOperatingUnit):
    def setUp(self):
        super().setUp()
        self.warehouse_b2b = self.env.ref("stock_operating_unit.stock_warehouse_b2b")
        self.picking_type2 = self.env["stock.picking.type"].search(
            [
                ("code", "=", "incoming"),
                ("warehouse_id", "=", self.warehouse_b2b.id),
            ],
            limit=1,
        )
        # Add permission b2b operating unit in user1
        self.b2b = self.env.ref("operating_unit.b2b_operating_unit")
        user = self.env["res.users"].browse(self.user1_id)
        user.operating_unit_ids = [(4, self.b2b.id)]

    def test_01_purchase_stock_operating_unit(self):
        self.assertEqual(self.purchase1.state, "purchase")
        self.assertEqual(
            self.purchase1.picking_ids.operating_unit_id,
            self.purchase1.picking_type_id.warehouse_id.operating_unit_id,
        )
        self.purchase1.button_cancel()
        self.purchase1.button_draft()
        # Check change picking type is not equal operating unit, it should error
        with self.assertRaises(UserError):
            with Form(self.purchase1) as po:
                po.picking_type_id = self.picking_type2
