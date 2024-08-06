# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class AgedPartnerBalanceReport(models.AbstractModel):
    _inherit = "report.account_financial_report.aged_partner_balance"

    def _get_report_values(self, docids, data):
        self = self.with_context(operating_unit_ids=data["operating_unit_ids"])
        return super()._get_report_values(docids, data)

    @api.model
    def _get_move_lines_domain_not_reconciled(
        self, company_id, account_ids, partner_ids, only_posted_moves, date_from
    ):
        domain = super()._get_move_lines_domain_not_reconciled(
            company_id, account_ids, partner_ids, only_posted_moves, date_from
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain
