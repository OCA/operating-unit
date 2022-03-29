# Copyright 2021 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    operating_unit_id = fields.Many2one(
        related="location_id.operating_unit_id",
        store=True,
    )
