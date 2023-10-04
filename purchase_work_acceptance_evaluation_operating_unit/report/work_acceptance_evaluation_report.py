# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class WorkAcceptanceEvaluationReport(models.Model):
    _inherit = "work.acceptance.evaluation.report"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
    )

    def _select(self):
        select_str = super()._select()
        select_str += """
            ,wa.operating_unit_id
        """
        return select_str
