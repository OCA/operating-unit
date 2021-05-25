# Copyright 2017 Open For Small Business Ltd
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_sellers(self, params):
        sellers = super()._prepare_sellers(params)
        if self._context.get("operating_unit_id"):
            sellers = sellers.filtered(
                lambda r: not r.operating_unit_id
                or r.operating_unit_id == self._context["operating_unit_id"]
            )
        return sellers


class SupplierInfo(models.Model):
    _inherit = "product.supplierinfo"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        index=True,
    )
