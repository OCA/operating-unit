# © 2016 Forgeflow S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import SUPERUSER_ID
from odoo.exceptions import UserError
from odoo.tests.common import Form, TransactionCase


class TestPurchaseRequestToRequisition(TransactionCase):
    def setUp(self):
        super(TestPurchaseRequestToRequisition, self).setUp()
        self.purchase_request = self.env["purchase.request"]
        self.purchase_request_line_obj = self.env["purchase.request.line"]
        self.wiz = self.env["purchase.request.line.make.purchase.requisition"]
        self.purchase_order = self.env["purchase.order"]
        # Main Operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        self.b2c = self.env.ref("operating_unit.b2c_operating_unit")
        # Products
        self.product1 = self.env.ref("product.product_product_9")
        self.purchase_request = self._create_purchase_request()

    def _create_purchase_request(self):
        vals = {
            "picking_type_id": self.env.ref("stock.picking_type_in").id,
            "requested_by": SUPERUSER_ID,
            "operating_unit_id": self.ou1.id,
            "line_ids": [
                (
                    0,
                    0,
                    {
                        "product_id": self.product1.id,
                        "product_uom_id": self.env.ref("uom.product_uom_unit").id,
                        "product_qty": 5.0,
                    },
                )
            ],
        }
        return self.purchase_request.create(vals)

    def test_purchase_request_to_purchase_requisition(self):
        # Test multi purchase request with diff operating unit
        self.purchase_request2 = self._create_purchase_request()
        picking_type = self.env["stock.picking.type"].search(
            [
                ("code", "=", "incoming"),
                ("warehouse_id.operating_unit_id", "=", self.b2c.id),
            ],
            limit=1,
        )
        with Form(self.purchase_request2) as pr:
            pr.picking_type_id = picking_type
            pr.operating_unit_id = self.b2c
        pr.save()
        self.purchase_request_line = self.purchase_request.line_ids
        # Lines with difference ou, should error
        with self.assertRaises(UserError):
            self.wiz.with_context(
                active_model="purchase.request.line",
                active_ids=[
                    self.purchase_request_line.id,
                    self.purchase_request2.line_ids.id,
                ],
            ).create({})
        # Check send context with purchase.request
        wiz = self.wiz.with_context(
            active_model="purchase.request",
            active_ids=[self.purchase_request.id],
        ).create({})
        wiz.make_purchase_requisition()
        requisition_id = self.purchase_request_line.requisition_lines.requisition_id
        self.assertEqual(
            requisition_id.operating_unit_id,
            self.purchase_request_line.operating_unit_id,
            "Should have the same Operating Unit",
        )
