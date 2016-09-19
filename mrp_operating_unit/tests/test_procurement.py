# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.tests import common


class TestProcurement(common.TransactionCase):

    def setUp(self):
        super(TestProcurement, self).setUp()
        self.res_users_model = self.env['res.users']
        self.procurement_order_model = self.env['procurement.order']
        self.procurement_rule_model = self.env['procurement.rule']
        self.mrp_line_model = self.env['mrp.bom.line']
        self.bom_model = self.env['mrp.bom']
        self.property_model = self.env['mrp.property']
        self.product_model = self.env['product.product']
        self.product_template_model = self.env['product.template']
        self.product_category_model = self.env['product.category']
        self.product_category = self.env.ref('product.product_category_2')
        self.warehouse = self.env.ref('stock.warehouse0')
        self.product_unit = self.env.ref('product.product_uom_unit')
        self.property = self.env.ref('mrp.mrp_property_0')
        self.line = self.env.ref('mrp.mrp_property_0')
        self.group = self.env.ref('mrp.mrp_property_group_1')
        self.company = self.env.ref('base.main_company')

        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')

        # Products
        self.product1 = self.env.ref('product.product_product_9')

        self.rule = self._create_procurement_rule()
        self.mrp_bom_method = self._create_bom()
        self.procurement_order = self._create_procurement_order()


    def _create_procurement_rule(self):
        rule = self.procurement_rule_model.create({
                'name': 'Procurement rule',
                'action': 'manufacture'
                })
        return rule

    def _create_bom(self):
        bom = self.bom_model.create({
                'product_tmpl_id': self.product1.product_tmpl_id.id,
                'product_id': self.product1.id,
                'product_qty': '1',
                'type': 'normal',
                'product_efficiency': '1.00',
        })
        return bom

    def _create_procurement_order(self):
        # On change for warehouse_id
        new_line = self.procurement_order_model.new()
        res = new_line.change_warehouse_id(self.warehouse.id)
        if res.get('value') and res.get('value').get('location_id'):
            location_id = res.get('value').get('location_id')
        # On change for product_id
        new_line = self.procurement_order_model.new()
        res = new_line.onchange_product_id(self.product1.id)
        if res.get('value') and res.get('value').get('product_uom'):
            product_uom = res.get('value').get('product_uom')
        order = self.procurement_order_model.create({
                'product_id': self.product1.id,
                'product_uom': product_uom,
                'product_qty': '10',
                'name': 'Procurement Order',
                'warehouse_id': self.warehouse.id,
                'bom_id': self.mrp_bom_method.id,
                'rule_id': self.rule.id,
                'location_id': location_id,
        })
        return order

    def test_security(self):
        self.assertEqual(self.procurement_order.location_id.operating_unit_id,
                         self.procurement_order.production_id.operating_unit_id,
                         'The Operating Unit in Procurement Order Location'
                         'does not match to Manufacturing Order OU.')
