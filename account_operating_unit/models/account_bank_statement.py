# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.model
    def _prepare_liquidity_move_line_vals(self):
        res = super()._prepare_liquidity_move_line_vals()
        res["operating_unit_id"] = self.statement_id.journal_id.operating_unit_id.id
        return res

    @api.model
    def _prepare_counterpart_move_line_vals(self, counterpart_vals, move_line=None):
        res = super()._prepare_counterpart_move_line_vals(counterpart_vals, move_line)
        res["operating_unit_id"] = self.statement_id.journal_id.operating_unit_id.id
        return res
