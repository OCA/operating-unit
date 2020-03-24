# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrderQuoteLine(models.Model):
    _name = 'sale.order.quote.line'
    _description = 'Internal Quote Line'

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
    def onchange_product_id(self):
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
    @api.onchange('qty', 'price_unit')
    def _onchange_qty(self):
        if self.qty:
            self.subtotal = self.price_unit * self.qty
