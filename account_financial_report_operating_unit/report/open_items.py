# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class OpenItemsReport(models.AbstractModel):
    _inherit = "report.account_financial_report.open_items"

    def _get_report_values(self, docids, data):
        self = self.with_context(operating_unit_ids=data["operating_unit_ids"])
        return super()._get_report_values(docids, data)

    @api.model
    def _get_move_lines_domain_not_reconciled(
        self, company_id, account_ids, partner_ids, target_move, date_from
    ):
        domain = super()._get_move_lines_domain_not_reconciled(
            company_id, account_ids, partner_ids, target_move, date_from
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain

    @api.model
    def _get_new_move_lines_domain(
        self, new_ml_ids, account_ids, company_id, partner_ids, target_moves
    ):
        domain = super()._get_new_move_lines_domain(
            new_ml_ids, account_ids, company_id, partner_ids, target_moves
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain
