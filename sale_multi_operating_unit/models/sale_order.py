# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    quote_ids = fields.One2many(
        'sale.order.quote', 'sale_id', string='Internal Quotes')
