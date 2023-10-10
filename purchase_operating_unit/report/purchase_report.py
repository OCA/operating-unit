# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        readonly=True,
    )

    def _select(self):
        select_str = super()._select()
        select_str += """, po.operating_unit_id"""
        return select_str

    def _group_by(self):
        group_by_str = super()._group_by()
        group_by_str += """, po.operating_unit_id"""
        return group_by_str
