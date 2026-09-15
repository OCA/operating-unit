# Copyright 2025 Camptocamp SA
# License: LGPL-3 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ProductPricelist(models.Model):
    _inherit = "product.pricelist"

    @api.model
    def _get_default_operating_unit(self):
        return self.env["res.users"]._get_default_operating_unit()

    operating_unit_id = fields.Many2one(
        "operating.unit",
        default=lambda self: self._get_default_operating_unit(),
        check_company=True,
    )
