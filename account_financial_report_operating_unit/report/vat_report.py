# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class VATReport(models.AbstractModel):
    _inherit = "report.account_financial_report.vat_report"

    def _get_report_values(self, docids, data):
        self = self.with_context(operating_unit_ids=data["operating_unit_ids"])
        return super()._get_report_values(docids, data)

    @api.model
    def _get_tax_report_domain(self, company_id, date_from, date_to, only_posted_moves):
        domain = super()._get_tax_report_domain(
            company_id, date_from, date_to, only_posted_moves
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain

    @api.model
    def _get_net_report_domain(self, company_id, date_from, date_to, only_posted_moves):
        domain = super()._get_net_report_domain(
            company_id, date_from, date_to, only_posted_moves
        )
        operating_unit_ids = self.env.context.get("operating_unit_ids", [])
        if operating_unit_ids:
            domain.append(("operating_unit_id", "in", operating_unit_ids))
        return domain
