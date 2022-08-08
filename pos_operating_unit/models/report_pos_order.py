# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ReportPosOrder(models.Model):
    _inherit = "report.pos.order"

    operating_unit_id = fields.Many2one("operating.unit", readonly=True)

    def _select(self):
        res = super()._select()
        res += ",l.operating_unit_id AS operating_unit_id"
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ",l.operating_unit_id"
        return res
