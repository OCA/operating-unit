# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    @api.depends("user_id", "company_id", "operating_unit_id")
    def _compute_warehouse_id(self):
        res = super()._compute_warehouse_id()
        for sale in self:
            if sale.warehouse_id.operating_unit_id != sale.operating_unit_id:
                warehouse = self.env["stock.warehouse"].search(
                    [
                        (
                            "operating_unit_id",
                            "=",
                            sale.operating_unit_id.id,
                        ),
                    ],
                    limit=1,
                )
                if warehouse:
                    sale.warehouse_id = warehouse.id
        return res

    @api.constrains("operating_unit_id", "warehouse_id")
    def _check_wh_operating_unit(self):
        for rec in self:
            if (
                rec.warehouse_id.operating_unit_id
                and rec.operating_unit_id
                and rec.operating_unit_id != rec.warehouse_id.operating_unit_id
            ):
                raise ValidationError(
                    self.env._(
                        "Configuration error!\nThe Operating"
                        "Unit in the Sales Order and in the"
                        " Warehouse must be the same."
                    )
                )
