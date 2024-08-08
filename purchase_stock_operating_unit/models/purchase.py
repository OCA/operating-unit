# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange("operating_unit_id")
    def _onchange_operating_unit_id(self):
        if self.operating_unit_id:
            self.picking_type_id = self.env["stock.picking.type"].search(
                [
                    ("warehouse_id.operating_unit_id", "=", self.operating_unit_id.id),
                    ("code", "=", "incoming"),
                ],
                limit=1,
            )

    @api.onchange("picking_type_id")
    def _onchange_picking_type_id(self):
        if self.picking_type_id:
            self.operating_unit_id = self.picking_type_id.warehouse_id.operating_unit_id

    @api.constrains("operating_unit_id", "picking_type_id")
    def _check_operating_unit_picking_type(self):
        for rec in self:
            if (
                rec.operating_unit_id
                and rec.operating_unit_id
                != rec.picking_type_id.warehouse_id.operating_unit_id
            ):
                raise UserError(
                    _(
                        "Configuration error. The Operating Unit in "
                        "the Purchase and Deliver To must be the same."
                    )
                )
