# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common
from odoo.exceptions import ValidationError


class TestProcurement(common.TransactionCase):

    def setUp(self):
        super(TestProcurement, self).setUp()
        self.procurement_order_model = self.env['procurement.order']
        self.procurement_rule_model = self.env['procurement.rule']
        self.bom_model = self.env['mrp.bom']
        self.warehouse = self.env.ref('stock.warehouse0')
        self.picking_type = self.env.ref('stock.picking_type_internal')

        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')

        # Products
        self.product1 = self.env.ref('product.product_product_9')

        # Stock Location
        self.stock_location_1 = self.env.ref('stock.stock_location_shop0')
        self.stock_location_2 = self.env.ref('stock.stock_location_14')

        self.rule = self._create_procurement_rule()
        self.mrp_bom_method = self._create_bom()
        self.procurement_order = self._create_procurement_order()
        self.procurement_order.run()

    def _create_procurement_rule(self):
        rule = self.procurement_rule_model.create({
            'name': 'Procurement rule',
            'action': 'manufacture',
            'picking_type_id': self.picking_type.id,
        })
        return rule

    def _create_bom(self):
        bom = self.bom_model.create({
            'product_tmpl_id': self.product1.product_tmpl_id.id,
            'product_id': self.product1.id,
            'product_qty': '1',
            'type': 'normal',
        })
        return bom

    def _create_procurement_order(self):
        order = self.procurement_order_model.create({
            'product_id': self.product1.id,
            'product_uom': self.product1.uom_id.id,
            'product_qty': '10',
            'name': 'Procurement Order',
            'warehouse_id': self.warehouse.id,
            'bom_id': self.mrp_bom_method.id,
            'rule_id': self.rule.id,
            'location_id': self.stock_location_1.id,
        })
        return order

    def test_security(self):
        self.assertEqual(
            self.procurement_order.location_id.operating_unit_id,
            self.procurement_order.production_id.operating_unit_id,
            'The Operating Unit in Procurement Order Location'
            'does not match to Manufacturing Order OU.'
        )

        with self.assertRaises(ValidationError):
            self.procurement_order.write({'location_id':
                                          self.stock_location_2.id})
