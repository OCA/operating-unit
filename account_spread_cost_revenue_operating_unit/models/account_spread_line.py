# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountInvoiceSpreadLine(models.Model):
    _inherit = "account.spread.line"

    def _prepare_move(self):
        move_vals = super()._prepare_move()
        if self.spread_id.operating_unit_id:
            move_vals.update({"operating_unit_id": self.spread_id.operating_unit_id.id})
        return move_vals
