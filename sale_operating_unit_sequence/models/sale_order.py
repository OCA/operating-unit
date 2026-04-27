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
    def _update_sale_order_name(self, vals):
        """Update sale order name in vals if operating unit has a sequence."""
        operating_unit_id = vals.get("operating_unit_id")
        if operating_unit_id:
            ou_id = self.env["operating.unit"].browse(operating_unit_id)
            name = ou_id._get_next_sale_order_number()
            if name:
                vals["name"] = name
        return vals
