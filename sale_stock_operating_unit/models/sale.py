# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
from openerp.tools.translate import _


class SaleShop(orm.Model):
    _inherit = 'sale.shop'

    def _check_warehouse_operating_unit(self, cr, uid, ids, context=None):
        for r in self.browse(cr, uid, ids, context=context):
            if r.warehouse_id and r.operating_unit_id and \
                    r.warehouse_id.operating_unit_id != r.operating_unit_id:
                return False
        return True

    _constraints = [
        (_check_warehouse_operating_unit,
         'The Operating Unit in the Warehouse must be the same as in the '
         'Sale Shop.', ['operating_unit_id', 'warehouse_id'])]


class SaleOrder(orm.Model):
    _inherit = 'sale.order'

    def _prepare_order_picking(self, cr, uid, order, context=None):
        res = super(SaleOrder, self)._prepare_order_picking(cr, uid, order,
                                                            context=context)
        if order.operating_unit_id:
            res.update({
                'operating_unit_id': order.operating_unit_id.id
            })

        return res
