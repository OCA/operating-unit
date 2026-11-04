# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class StockRule(models.Model):
    _inherit = "stock.rule"

    def _prepare_purchase_order(self, company_id, origins, values):
        res = super()._prepare_purchase_order(company_id, origins, values)
        if self.operating_unit_id:
            res["operating_unit_id"] = self.operating_unit_id.id
            res["requesting_operating_unit_id"] = self.operating_unit_id.id
        elif ou_id := values[0].get("operating_unit_id"):
            res["operating_unit_id"] = res["requesting_operating_unit_id"] = ou_id
        return res
