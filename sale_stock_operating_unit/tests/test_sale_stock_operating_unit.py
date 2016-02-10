# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import netsvc
from openerp.addons.sale_operating_unit.tests import test_sale_operating_unit


class TestSaleStockOperatingUnit(test_sale_operating_unit.
                                 TestSaleOperatingUnit):

    def setUp(self):
        super(TestSaleStockOperatingUnit, self).setUp()
        cr, uid, context = self.cr, self.uid, {}
        data_model = self.registry('ir.model.data')
        self.warehouse_model = self.registry('stock.warehouse')
        # B2C Warehouse
        self.warehouse2 = data_model.get_object(cr, uid,
                                                'stock_operating_unit',
                                                'stock_warehouse_b2c')
        # Create Shop2
        self.new_shop2_id = self._update_shops(cr, self.user2_id,
                                               self.shop2_id, self.warehouse2,
                                               context=context)
        self.stock_pick_model = self.registry('stock.picking.out')
#        # Create Sale Order2
        self.new_sale2_id = self._update_sale_order(cr, self.user2_id,
                                                    self.sale2_id,
                                                    self.new_shop2_id,
                                                    context=context)

    def _update_shops(self, cr, uid, shop_id, warehouse, context=None):
        """Create a shop."""
        self.shop_model.write(cr, uid, [shop_id], {
            'warehouse_id': warehouse.id,
        })
        shop = self.shop_model.browse(cr, uid, shop_id)
        new_shop_id = shop.id
        return new_shop_id

    def _update_sale_order(self, cr, uid, sale_id, shop, context=None):
        """Create a sale order."""
        self.sale_model.write(cr, uid, [sale_id], {
            'shop_id': shop,
        })
        sale = self.sale_model.browse(cr, uid, sale_id)
        new_sale_id = sale.id
        return new_sale_id

    def _confirm_sale(self, cr, uid, sale_id):
        self.sale_model.action_button_confirm(cr, uid, [sale_id])
        sale = self.sale_model.browse(cr, uid, sale_id)
        for picking in sale.picking_ids:
            self.operating_unit = picking.operating_unit_id
        return sale

    def test_security(self):
        """Test Sale Operating Unit"""
        # User 2 is only assigned to Operating Unit B2C, and cannot
        # Access Sales order from Main Operating Unit.
        cr, uid = self.cr, self.uid
        sale_ids = self.sale_model.search(self.cr, self.user2_id,
                                         [('operating_unit_id', '=',
                                           self.ou1.id)])
        self.assertEqual(sale_ids, [], 'User 2 should not have access to '
                                       'OU %s' % self.ou1.name)
        # Confirm Sale1
        sale1 = self._confirm_sale(cr, uid, self.sale1_id)
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(self.operating_unit, sale1.operating_unit_id,
                         'OU in Sale Order and Picking should be same')
        # Confirm Sale2
        sale2 = self._confirm_sale(cr, uid, self.new_sale2_id)
        # Checks that OU in sale order and stock picking matches or not.
        self.assertEqual(self.operating_unit, sale2.operating_unit_id,
                         'OU in Sale Order and Picking should be same')
