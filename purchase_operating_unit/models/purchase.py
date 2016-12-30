# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import _, api, exceptions, fields, models
from openerp.exceptions import Warning


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.model
    def _default_picking_type(self):
        res = super(PurchaseOrder, self)._default_picking_type()
        type_obj = self.env['stock.picking.type']
        operating_unit = self.env['res.users'].operating_unit_default_get(
                self._uid)
        types = type_obj.search([('code', '=', 'incoming'),
                                 ('warehouse_id.operating_unit_id', '=',
                                  operating_unit.id)])
        if types:
            res = types[:1].id
        return res

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))
    requesting_operating_unit_id =\
        fields.Many2one('operating.unit', 'Requesting Operating Unit',
                        default=lambda self:
                        self.env['res.users'].
                        operating_unit_default_get(self._uid))

    picking_type_id = fields.Many2one('stock.picking.type', 'Deliver To',
                                      help="This will determine picking type "
                                           "of incoming shipment",
                                      required=True,
                                      states={'confirmed':
                                              [('readonly', True)],
                                              'approved': [('readonly', True)],
                                              'done': [('readonly', True)]},
                                      default=_default_picking_type)

    @api.one
    @api.constrains('operating_unit_id', 'picking_type_id')
    def _check_warehouse_operating_unit(self):
        picking_type = self.picking_type_id
        if picking_type:
            if picking_type.warehouse_id and\
                    picking_type.warehouse_id.operating_unit_id\
                    and self.operating_unit_id and\
                    picking_type.warehouse_id.operating_unit_id !=\
                    self.operating_unit_id:
                raise Warning(_('Configuration error!\nThe\
                Quotation / Purchase Order and the Warehouse of picking type\
                must belong to the same Operating Unit.'))

    @api.one
    @api.constrains('operating_unit_id', 'requesting_operating_unit_id',
                    'company_id')
    def _check_company_operating_unit(self):
        if self.company_id and self.operating_unit_id and\
                self.company_id != self.operating_unit_id.company_id:
            raise Warning(_('Configuration error!\nThe Company in the\
            Purchase Order and in the Operating Unit must be the same.'))

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
                raise exceptions.Warning(_("No Warehouse found with the "
                                           "Operating Unit indicated in the "
                                           "Purchase Order!"))

    @api.model
    def _prepare_picking(self):
        picking_vals = super(PurchaseOrder, self)._prepare_picking()
        picking_vals['operating_unit_id'] = self.operating_unit_id and\
            self.operating_unit_id.id
        return picking_vals

    @api.one
    @api.constrains('invoice_ids')
    def _check_invoice_ou(self):
        for po in self:
            for invoice in po.invoice_ids:
                if invoice.operating_unit_id != po.operating_unit_id:
                    raise Warning(_('The operating unit of the purchase order '
                                    'must be the same as in the '
                                    'associated invoices.'))


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    operating_unit_id = fields.Many2one('operating.unit',
                                        related='order_id.operating_unit_id',
                                        string='Operating Unit', readonly=True)

    @api.one
    @api.constrains('invoice_lines')
    def _check_invoice_ou(self):
        for line in self:
            for inv_line in line.invoice_lines:
                if inv_line.invoice_id and \
                    inv_line.invoice_id.operating_unit_id != \
                        line.operating_unit_id:
                    raise Warning(_('The operating unit of the purchase order '
                                    'must be the same as in the '
                                    'associated invoices.'))
