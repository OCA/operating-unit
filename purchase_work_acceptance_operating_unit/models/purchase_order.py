# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def action_view_wa(self):
        result = super().action_view_wa()
        if self.operating_unit_id:
            result["context"]["default_operating_unit_id"] = self.operating_unit_id.id
        return result
