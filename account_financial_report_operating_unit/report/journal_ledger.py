# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class JournalLedgerReport(models.AbstractModel):
    _inherit = "report.account_financial_report.journal_ledger"

    def _get_report_values(self, docids, data):
        self = self.with_context(operating_unit_ids=data["operating_unit_ids"])
        return super()._get_report_values(docids, data)

    def _get_move_lines_domain(self, move_ids, wizard, journal_ids):
        domain = super()._get_move_lines_domain(move_ids, wizard, journal_ids)
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain
