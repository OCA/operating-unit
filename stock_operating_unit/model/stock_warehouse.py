# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.exceptions import UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    @api.model
    def _default_operating_unit(self, company=False):
        company = company or self.env.company
        default_ou = self.env.user.default_operating_unit_id.sudo()
        if default_ou.company_id == company:
            return default_ou
        return self.env.user.operating_unit_ids.sudo().filtered(
            lambda ou: ou.company_id == company
        )[:1]

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if "operating_unit_id" not in vals:
                company = self.env["res.company"].browse(vals.get("company_id"))
                operating_unit = self._default_operating_unit(company)
                vals["operating_unit_id"] = (
                    operating_unit.id if operating_unit else False
                )
        return super().create(vals_list)

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=lambda self: self._default_operating_unit(),
        check_company=True,
    )


class StockWarehouseOrderPoint(models.Model):
    _inherit = "stock.warehouse.orderpoint"

    @api.constrains(
        "warehouse_id",
        "location_id",
    )
    def _check_location(self):
        for rec in self:
            if (
                rec.warehouse_id.operating_unit_id
                and rec.warehouse_id
                and rec.location_id
                and rec.warehouse_id.operating_unit_id
                != rec.location_id.operating_unit_id
            ):
                raise UserError(
                    self.env._(
                        "Configuration Error. The Operating Unit of the "
                        "Warehouse and the Location must be the same. "
                    )
                )
