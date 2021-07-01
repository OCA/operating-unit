# Copyright 2021 O4SB Ltd - Rujia Liu
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class StockValuationLayer(models.Model):
    """Stock Valuation Layer"""

    _inherit = "stock.valuation.layer"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        readonly=True,
    )
