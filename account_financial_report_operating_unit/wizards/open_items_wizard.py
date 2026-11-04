# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OpenItemsReportWizard(models.TransientModel):
    _inherit = "open.items.report.wizard"

    operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
    )

    def _prepare_report_open_items(self):
        res = super()._prepare_report_open_items()
        res.update({"operating_unit_ids": self.operating_unit_ids.ids or []})
        return res
