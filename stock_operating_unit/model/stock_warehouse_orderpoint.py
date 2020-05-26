# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class StockWarehouseOrderpoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )
