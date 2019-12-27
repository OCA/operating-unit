# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quote_ids = fields.One2many(
        'sale.order.quote', 'sale_id', string='Internal Quotes')

    @api.model
    def create(self, vals):
        res = super().create(vals)
        if res.quote_ids:
            for quote in res.quote_ids:
                quote.name = quote.sale_id.name
        return res
