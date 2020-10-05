# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockLocation(models.Model):
    _inherit = "stock.location"

    operating_unit_id = fields.Many2one("operating.unit", "Operating Unit")

    @api.constrains("operating_unit_id")
    def _check_warehouse_operating_unit(self):
        for rec in self:
            warehouse_obj = self.env["stock.warehouse"]
            warehouses = warehouse_obj.search(
                [
                    "|",
                    "|",
                    ("wh_input_stock_loc_id", "=", rec.ids[0]),
                    ("lot_stock_id", "in", rec.ids),
                    ("wh_output_stock_loc_id", "in", rec.ids),
                ]
            )
            for w in warehouses:
                if rec.operating_unit_id != w.operating_unit_id:
                    raise UserError(
                        _(
                            "Configuration error. This location is "
                            "assigned to a warehouse that belongs to"
                            " a different operating unit."
                        )
                    )

    @api.constrains("operating_unit_id")
    def _check_required_operating_unit(self):
        for rec in self:
            if rec.usage not in ("supplier", "customer") and not rec.operating_unit_id:
                raise UserError(
                    _(
                        "Configuration error. The operating unit should be "
                        "assigned to internal locations only."
                    )
                )
            if rec.usage in ("supplier", "customer") and rec.operating_unit_id:
                raise UserError(
                    _(
                        "Configuration error. The operating unit should be "
                        "assigned to internal locations only."
                    )
                )

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for rec in self:
            if (
                rec.company_id
                and rec.operating_unit_id
                and rec.company_id != rec.operating_unit_id.company_id
            ):
                raise UserError(
                    _(
                        "Configuration error. The Company in the Stock Location "
                        "and in the Operating Unit must be the same."
                    )
                )

    @api.constrains("operating_unit_id", "location_id")
    def _check_parent_operating_unit(self):
        for rec in self:
            if (
                rec.location_id
                and rec.location_id.usage == "internal"
                and rec.operating_unit_id
                and rec.operating_unit_id != rec.location_id.operating_unit_id
            ):
                raise UserError(
                    _(
                        "Configuration error. The Parent Stock Location "
                        "must belong to the same Operating Unit."
                    )
                )
