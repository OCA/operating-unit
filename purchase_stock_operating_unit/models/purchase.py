# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    picking_type_id = fields.Many2one(
        compute="_compute_picking_type_id", store=True, readonly=False
    )
    operating_unit_id = fields.Many2one(
        compute="_compute_operating_unit_id",
        store=True,
        readonly=False,
    )

    @api.depends("operating_unit_id")
    def _compute_picking_type_id(self):
        for purchase in self:
            if purchase.operating_unit_id:
                purchase.picking_type_id = self.env["stock.picking.type"].search(
                    [
                        (
                            "warehouse_id.operating_unit_id",
                            "=",
                            purchase.operating_unit_id.id,
                        ),
                        ("code", "=", "incoming"),
                    ],
                    limit=1,
                )

    @api.depends("picking_type_id")
    def _compute_operating_unit_id(self):
        for purchase in self:
            if purchase.picking_type_id:
                purchase.operating_unit_id = (
                    purchase.picking_type_id.warehouse_id.operating_unit_id
                )

    @api.constrains("operating_unit_id", "picking_type_id")
    def _check_operating_unit_picking_type(self):
        for rec in self:
            if (
                rec.operating_unit_id
                and rec.picking_type_id.warehouse_id.operating_unit_id
                and rec.operating_unit_id
                != rec.picking_type_id.warehouse_id.operating_unit_id
            ):
                raise UserError(
                    _(
                        "Configuration error. The Operating Unit in "
                        "the Purchase and Deliver To must be the same."
                    )
                )

    def _prepare_picking(self):
        vals = super()._prepare_picking()
        vals["operating_unit_id"] = self.operating_unit_id.id
        return vals
