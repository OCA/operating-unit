# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class SaleReport(models.Model):
    _inherit = "sale.report"

    operating_unit_id = fields.Many2one("operating.unit", readonly=True)

    def _select_dict(self, table):
        return super()._select_dict(table) | {
            "operating_unit_id": table.order_id.operating_unit_id
        }
