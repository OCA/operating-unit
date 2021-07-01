# Copyright 2021 O4SB Ltd - Rujia Liu
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def _prepare_in_svl_vals(self, quantity, unit_cost):
        vals = super()._prepare_in_svl_vals(quantity, unit_cost)
        self.ensure_one()
        dest_operating_unit = self._context.get("operating_unit")
        if dest_operating_unit:
            vals.update({"operating_unit_id": dest_operating_unit})
        return vals

    def _prepare_out_svl_vals(self, quantity, company):
        vals = super()._prepare_out_svl_vals(quantity, company)
        self.ensure_one()
        source_operating_unit = self._context.get("operating_unit")
        if source_operating_unit:
            vals.update({"operating_unit_id": source_operating_unit})
        return vals
