# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.model
    def create(self, vals):
        if vals.get("name", "/") == "/" and vals.get("operating_unit_id", False):
            ou_id = self.env["operating.unit"].browse(vals["operating_unit_id"])
            if ou_id.sale_sequence_id:
                vals["name"] = ou_id.sale_sequence_id.next_by_id()
        return super().create(vals)
