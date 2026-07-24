# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        """Override create to update name based on operating unit sequence."""
        if vals.get("name", "/") == "/":
            vals = self._update_sale_order_name(vals)
        return super().create(vals)

    @api.model
    def _get_sequence_operating_unit_id(self, vals):
        """Resolve the operating unit to use for sequence generation,
        falling back to the field's default when it is missing from vals."""
        if "operating_unit_id" in vals:
            # Key present, even if falsy: the caller explicitly requested no
            # operating unit, so do not override it with the default.
            operating_unit_id = vals["operating_unit_id"]
        else:
            operating_unit_id = self.default_get(["operating_unit_id"]).get(
                "operating_unit_id"
            )
        return operating_unit_id

    @api.model
    def _update_sale_order_name(self, vals):
        """Update sale order name in vals if operating unit has a sequence."""
        operating_unit_id = self._get_sequence_operating_unit_id(vals)
        if operating_unit_id:
            ou_id = self.env["operating.unit"].browse(operating_unit_id)
            name = ou_id._get_next_sale_order_number()
            if name:
                vals["name"] = name
        return vals
