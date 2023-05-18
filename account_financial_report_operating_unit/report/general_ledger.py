# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class GeneralLedgerReport(models.AbstractModel):
    _inherit = "report.account_financial_report.general_ledger"

    def _get_report_values(self, docids, data):
        self = self.with_context(operating_unit_ids=data["operating_unit_ids"])
        return super()._get_report_values(docids, data)

    def _get_initial_balances_bs_ml_domain(
        self, account_ids, company_id, date_from, base_domain, grouped_by, acc_prt=False
    ):
        domain = super()._get_initial_balances_bs_ml_domain(
            account_ids, company_id, date_from, base_domain, grouped_by, acc_prt=acc_prt
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain

    def _get_initial_balances_pl_ml_domain(
        self, account_ids, company_id, date_from, fy_start_date, base_domain
    ):
        domain = super()._get_initial_balances_pl_ml_domain(
            account_ids, company_id, date_from, fy_start_date, base_domain
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain

    def _get_initial_balance_fy_pl_ml_domain(
        self, account_ids, company_id, fy_start_date, base_domain
    ):
        domain = super()._get_initial_balance_fy_pl_ml_domain(
            account_ids, company_id, fy_start_date, base_domain
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain

    @api.model
    def _get_period_domain(
        self,
        account_ids,
        partner_ids,
        company_id,
        only_posted_moves,
        date_to,
        date_from,
        analytic_tag_ids,
        cost_center_ids,
    ):
        domain = super()._get_period_domain(
            account_ids,
            partner_ids,
            company_id,
            only_posted_moves,
            date_to,
            date_from,
            analytic_tag_ids,
            cost_center_ids,
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain
