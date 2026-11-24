# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, fields, models
from odoo.tools import SQL


class TimesheetsAnalysisReport(models.Model):
    _inherit = "timesheets.analysis.report"

    operating_unit_id = fields.Many2one("operating.unit", readonly=True)

    @api.model
    def _select(self):
        return SQL("%s, A.operating_unit_id AS operating_unit_id", super()._select())
