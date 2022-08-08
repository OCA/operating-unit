# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    def _prepare_picking_vals(
        self, partner, picking_type, location_id, location_dest_id
    ):
        res = super()._prepare_picking_vals(
            partner, picking_type, location_id, location_dest_id
        )
        res["operating_unit_id"] = picking_type.warehouse_id.operating_unit_id.id
        return res
