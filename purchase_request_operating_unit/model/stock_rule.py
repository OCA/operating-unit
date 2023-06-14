# Copyright 2023 ForgeFlow, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0)

from odoo import api, models


class StockRule(models.Model):
    _inherit = "stock.rule"

    @api.model
    def _prepare_purchase_request(self, origin, values):
        res = super(StockRule, self)._prepare_purchase_request(origin, values)
        if self.warehouse_id.operating_unit_id:
            res.update({"operating_unit_id": self.warehouse_id.operating_unit_id.id})
        return res
