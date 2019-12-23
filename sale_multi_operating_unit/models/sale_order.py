# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


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
