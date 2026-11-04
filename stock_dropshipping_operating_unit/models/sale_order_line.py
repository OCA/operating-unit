# Copyright 2026 Luc De Meyer
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    def _prepare_procurement_values(self, group_id=False):
        values = super()._prepare_procurement_values(group_id=group_id)
        if self.order_id.operating_unit_id:
            values["operating_unit_id"] = self.order_id.operating_unit_id.id
        return values
