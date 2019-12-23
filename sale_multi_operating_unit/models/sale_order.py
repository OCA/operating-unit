# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrderQuote(models.Model):
    _name = 'sale.order.quote'

    name = fields.Char(string='Name')
    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        required=True
    )
    sale_id = fields.Many2one(
        comodel_name='sale.order',
        string='Sale'
    )
    lead_id = fields.Many2one(
        comodel_name='crm.lead',
        string='Lead',
        readonly=True
    )
    line_ids = fields.One2many(
        'sale.order.quote.line', 'quote_id', string='Products')
    state = fields.Selection([
        ('new', 'New'),
        ('sent', 'Sent'),
        ('received', 'Received')], string='State',
        copy=False, default='new', track_visibility='onchange')

    @api.onchange('operating_unit_id')
    def _onchange_operating_unit_id(self):
        if self.operating_unit_id:
            sale_id = self.env['sale.order'].browse(
                self._context.get('active_id'))
            if not sale_id:
                sale_id = self.env['sale.order']. \
                    browse(self._context.get('params')['id'])
            self.name = sale_id.name + ' - ' + self.operating_unit_id.code

    @api.onchange('state')
    def _onchange_state(self):
        lead_obj = self.env['crm.lead']
        if self.state and self.state == 'sent' and self.sale_id:
            lead_id = lead_obj.search([('partner_id', '=',
                                        self.sale_id.partner_id.id),
                                       ('stage_id', '=', 4)])
            if not lead_id:
                lead_id = lead_obj. \
                    create({
                           'partner_id': self.sale_id.partner_id.id,
                           'type': 'lead',
                           'user_id': self._uid,
                           'name': self.sale_id.name + ' - ' +
                           self.operating_unit_id.code
                           })
                self.lead_id = lead_id.id


class SaleOrderQuoteLine(models.Model):
    _name = 'sale.order.quote.line'

    name = fields.Char(string='Description', required=True)
    quote_id = fields.Many2one(
        comodel_name='sale.order.quote',
        string='Internal Quote'
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product'
    )
    qty = fields.Float(string="Quantity")
    uom_id = fields.Many2one(
        comodel_name='uom.uom',
        string='Unit of Measure'
    )
    price_unit = fields.Float(string="Unit Price")
    subtotal = fields.Float(string="Subtotal")

    @api.multi
    @api.onchange('product_id')
    def product_id_change(self):
        if not self.product_id:
            return {'domain': {'product_uom': []}}

        vals = {}
        domain = {'product_uom': [('category_id', '=',
                                   self.product_id.uom_id.category_id.id)]}
        if not self.uom_id or (self.product_id.uom_id.id != self.uom_id.id):
            vals['uom_id'] = self.product_id.uom_id
            vals['qty'] = self.qty or 1.0

        result = {'domain': domain}

        vals['price_unit'] = self.product_id.lst_price
        name = self.product_id.get_product_multiline_description_sale()
        vals.update(name=name)
        self.update(vals)
        return result

    @api.multi
    @api.onchange('qty')
    def _onchange_qty(self):
        if self.qty:
            self.subtotal = self.price_unit * self.qty


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quote_ids = fields.One2many(
        'sale.order.quote', 'sale_id', string='Internal Quotes')

    @api.constrains('quote_ids')
    def _operating_unit_id(self):
        operating_unit = [str(quote.operating_unit_id.id)
                          for quote in self.quote_ids]
        result = len(operating_unit) != len(set(operating_unit))
        if result:
            raise ValidationError(_(
                """The Operating Unit must be unique per sale order!"""))
