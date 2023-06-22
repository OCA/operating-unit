# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    operating_unit_id = fields.Many2one("operating.unit", "Operating Unit")

    def _group_by_sale(self):
        res = super()._group_by_sale()
        res += """, s.operating_unit_id"""
        return res

    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res["operating_unit_id"] = "s.operating_unit_id"
        return res
