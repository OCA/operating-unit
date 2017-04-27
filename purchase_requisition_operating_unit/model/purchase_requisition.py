# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import fields, models, api
from openerp.tools.translate import _
from openerp.exceptions import Warning as UserError


class PurchaseRequisition(models.Model):

    _inherit = 'purchase.requisition'

    @api.model
    def _get_picking_in(self):
        res = super(PurchaseRequisition, self)._get_picking_in()
        type_obj = self.env['stock.picking.type']
        operating_unit = self.env['res.users'].\
            operating_unit_default_get(self._uid)
        types = type_obj.search([('code', '=', 'incoming'),
                                 ('warehouse_id.operating_unit_id', '=',
                                  operating_unit.id)])
        if types:
            res = types[:1].id
        return res

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        readonly=True,
                                        states={'draft': [('readonly',
                                                           False)]},
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))

    picking_type_id = fields.Many2one('stock.picking.type', 'Picking Type',
                                      domain=[('code', '=', 'incoming')],
                                      required=True,
                                      default=_get_picking_in)

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if rec.company_id and rec.operating_unit_id and \
                    rec.company_id != rec.operating_unit_id.company_id:
                raise UserError(_('The Company in the Purchase Requisition and'
                                  ' in the Operating Unit must be the same.'))

    @api.multi
    @api.constrains('operating_unit_id', 'picking_type_id')
    def _check_warehouse_operating_unit(self):
        for rec in self:
            picking_type = rec.picking_type_id
            if picking_type:
                if picking_type.warehouse_id and\
                    picking_type.warehouse_id.operating_unit_id\
                    and rec.operating_unit_id and\
                    picking_type.warehouse_id.operating_unit_id !=\
                        rec.operating_unit_id:
                    raise UserError(_('Configuration error!\nThe Operating \
                    Unit in Purchase Requisition and the Warehouse of picking \
                    type must belong to the same Operating Unit.'))

    @api.onchange('operating_unit_id')
    def _onchange_operating_unit_id(self):
        type_obj = self.env['stock.picking.type']
        if self.operating_unit_id:
            types = type_obj.search([('code', '=', 'incoming'),
                                     ('warehouse_id.operating_unit_id', '=',
                                      self.operating_unit_id.id)])
            if types:
                self.picking_type_id = types[:1]
            else:
                raise UserError(_("No Warehouse found with the "
                                  "Operating Unit indicated in the "
                                  "Purchase Requisition!"))

    @api.model
    def _prepare_purchase_order(self, requisition, supplier):
        res = super(PurchaseRequisition, self).\
            _prepare_purchase_order(requisition, supplier)
        res.update({'operating_unit_id': requisition.operating_unit_id.id})
        return res


class PurchaseRequisitionLine(models.Model):
    _inherit = 'purchase.requisition.line'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        related='requisition_id.'
                                        'operating_unit_id',
                                        readonly=True, store=True)
