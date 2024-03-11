# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    def _prepare_stock_moves(self, picking):
        """Add operating unit from warehouse to picking"""
        picking.operating_unit_id = (
            picking.picking_type_id.warehouse_id.operating_unit_id
        )
        return super()._prepare_stock_moves(picking)
