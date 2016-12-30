# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.exceptions import ValidationError
from openerp.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))

    @api.onchange('team_id')
    def onchange_team_id(self):
        self.operating_unit_id = self.team_id.operating_unit_id

    @api.multi
    @api.constrains('team_id', 'operating_unit_id')
    def _check_team_operating_unit(self):
        for rec in self:
            if rec.team_id and rec.team_id.operating_unit_id != \
                    rec.operating_unit_id:
                raise ValidationError(_('Configuration error!\n'
                                        'The Operating Unit of the sales team '
                                        'must match with that of the '
                                        'quote/sales order'))

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if rec.company_id and rec.operating_unit_id and\
                    rec.company_id != rec.operating_unit_id.company_id:
                raise ValidationError(_('Configuration error!\nThe Company in'
                                        ' the Sales Order and in the Operating'
                                        ' Unit must be the same.'))

    @api.multi
    def _prepare_invoice(self):
        self.ensure_one()
        invoice_vals = super(SaleOrder, self)._prepare_invoice()
        invoice_vals['operating_unit_id'] = self.operating_unit_id.id
        return invoice_vals


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    operating_unit_id = fields.Many2one('operating.unit',
                                        related='order_id.operating_unit_id',
                                        string='Operating Unit',
                                        readonly=True)
