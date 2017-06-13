# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.tests import common
from openerp.tools import SUPERUSER_ID


class TestPurchaseRequestToRfq(common.TransactionCase):

    def setUp(self):
        super(TestPurchaseRequestToRfq, self).setUp()
        self.purchase_request = self.env['purchase.request']
        self.purchase_request_line = self.env['purchase.request.line']
        self.wiz =\
            self.env['purchase.request.line.make.purchase.order']
        self.purchase_order = self.env['purchase.order']
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # Products
        self.product1 = self.env.ref('product.product_product_9')
        self._create_purchase_request()

    def _create_purchase_request(self):
        vals = {
            'picking_type_id': self.env.ref('stock.picking_type_in').id,
            'requested_by': SUPERUSER_ID,
            'operating_unit_id': self.ou1.id
        }
        purchase_request = self.purchase_request.create(vals)
        vals = {
            'request_id': purchase_request.id,
            'product_id': self.product1.id,
            'product_uom_id': self.env.ref('product.product_uom_unit').id,
            'product_qty': 5.0,
        }
        self.purchase_request_line = self.purchase_request_line.create(vals)
        purchase_request.button_to_approve()
        purchase_request.button_approved()

    def test_purchase_request_to_purchase_requisition(self):
        vals = {'supplier_id': self.env.ref('base.res_partner_12').id}
        wiz_id = self.wiz.with_context(
            active_model="purchase.request.line",
            active_ids=[self.purchase_request_line.id],
            active_id=self.purchase_request_line.id,).create(vals)
        wiz_id.make_purchase_order()
        purchase_id = self.purchase_request_line.purchase_lines.order_id
        self.assertEqual(
            purchase_id.operating_unit_id,
            self.purchase_request_line.operating_unit_id,
            'Should have the same Operating Unit')
