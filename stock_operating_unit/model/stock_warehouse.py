# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    def _default_operating_unit(self):
        if self.company_id:
            company = self.company_id
        else:
            company = self.env.company
        for ou in self.env.user.operating_unit_ids:
            if company == self.company_id:
                self.operating_unit_id = ou

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=_default_operating_unit,
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
                    _(
                        "Configuration Error. The Operating Unit of the "
                        "Warehouse and the Location must be the same. "
                    )
                )
