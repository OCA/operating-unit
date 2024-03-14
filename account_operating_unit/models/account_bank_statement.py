# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        result = super()._prepare_move_line_default_vals(
            counterpart_account_id=counterpart_account_id
        )
        result[0][
            "operating_unit_id"
        ] = self.statement_id.journal_id.operating_unit_id.id
        result[1][
            "operating_unit_id"
        ] = self.statement_id.journal_id.operating_unit_id.id
        return result
