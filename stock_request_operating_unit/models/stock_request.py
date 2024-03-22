# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class StockRequest(models.Model):
    _inherit = "stock.request"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        compute="_compute_operating_unit",
        readonly=False,
        store=True,
    )

    @api.depends("order_id", "order_id.operating_unit_id")
    def _compute_operating_unit(self):
        default_operating_unit = self.env["res.users"].operating_unit_default_get(
            self.env.uid
        )
        for record in self:
            if record.order_id:
                record.operating_unit_id = record.order_id.operating_unit_id
            else:
                record.operating_unit_id = default_operating_unit

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for record in self:
            if (
                record.company_id
                and record.operating_unit_id
                and record.company_id != record.operating_unit_id.company_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Company in the Stock Request "
                        "and in the Operating Unit must be the same."
                    )
                )

    def _prepare_procurement_values(self, group_id=False):
        """
        Add operating unit to procurement values
        """
        res = super()._prepare_procurement_values(group_id=group_id)
        if self.operating_unit_id:
            res.update({"operating_unit_id": self.operating_unit_id.id})
        return res
