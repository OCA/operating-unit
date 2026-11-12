# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    @api.model_create_multi
    def create(self, vals_list):
        # OVERRIDE: set the journal OU before the delegated move is created.
        for vals in vals_list:
            if vals.get("operating_unit_id"):
                continue
            journal = self.env["account.journal"].browse(vals.get("journal_id"))
            if not journal and vals.get("statement_id"):
                statement = self.env["account.bank.statement"].browse(
                    vals["statement_id"]
                )
                journal = statement.journal_id
            if journal.operating_unit_id:
                vals["operating_unit_id"] = journal.operating_unit_id.id
        return super().create(vals_list)

    def _prepare_move_line_default_vals(self, counterpart_account_id=None):
        result = super()._prepare_move_line_default_vals(
            counterpart_account_id=counterpart_account_id
        )
        journal_operating_unit = self.journal_id.operating_unit_id
        result[0]["operating_unit_id"] = journal_operating_unit.id
        result[1]["operating_unit_id"] = journal_operating_unit.id
        return result
