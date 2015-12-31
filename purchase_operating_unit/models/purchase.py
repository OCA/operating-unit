# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.tools.translate import _
from openerp import api, fields, models
from openerp.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))
    requesting_operating_unit_id =\
        fields.Many2one('operating.unit', 'Requesting Operating Unit',
                        default=lambda self:
                        self.env['res.users'].
                        operating_unit_default_get(self._uid))

#    @api.one
#    @api.constrains('operating_unit_id', 'picking_type_id')
#    def _check_warehouse_operating_unit(self):
#        picking_type = self.picking_type_id
#        if picking_type:
#            if picking_type.warehouse_id and\
#                    picking_type.warehouse_id.operating_unit_id\
#                    and self.operating_unit_id and\
#                    picking_type.warehouse_id.operating_unit_id !=\
#                    self.operating_unit_id:
#                raise UserError(_('Configuration error!\nThe\
#                Quotation / Purchase Order and the Warehouse of picking type\
#                must belong to the same Operating Unit.'))

    @api.one
    @api.constrains('operating_unit_id', 'requesting_operating_unit_id',
                    'company_id')
    def _check_company_operating_unit(self):
        if self.company_id and self.operating_unit_id and\
                self.company_id != self.operating_unit_id.company_id:
            raise UserError(_('Configuration error!\nThe Company in the\
            Purchase Order and in the Operating Unit must be the same.'))

    @api.onchange('requesting_operating_unit_id', 'operating_unit_id')
    def onchange_operating_unit_id(self):
        pick_type = self.env['stock.picking.type']
        location_obj = self.env['stock.location']
        if not self.requesting_operating_unit_id or not self.operating_unit_id:
            return {}
        request_locations =\
            location_obj.search([('operating_unit_id', '=',
                                  self.requesting_operating_unit_id.id)])
        picking_types =\
            pick_type.search([('default_location_dest_id', 'in',
                               request_locations.ids)], limit=1)
        if picking_types:
            self.picking_type_id = picking_types.id

    @api.model
    def _prepare_picking(self):
        res = super(PurchaseOrder, self)._prepare_picking()
        res['operating_unit_id'] = self.operating_unit_id and\
            self.operating_unit_id.id
        return res


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    operating_unit_id = fields.Many2one('operating.unit',
                                        related='order_id.operating_unit_id',
                                        string='Operating Unit', readonly=True)
