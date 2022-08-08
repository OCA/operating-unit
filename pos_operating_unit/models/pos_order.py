# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PosOrder(models.Model):
    _inherit = "pos.order"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        readonly=True,
    )

    def _prepare_invoice_vals(self):
        vals = super()._prepare_invoice_vals()
        vals["operating_unit_id"] = self.operating_unit_id.id
        return vals

    @api.model
    def _order_fields(self, ui_order):
        res = super()._order_fields(ui_order)
        res["operating_unit_id"] = (
            self.env["pos.session"]
            .browse(ui_order["pos_session_id"])
            .operating_unit_id.id
        )
        return res

    @api.model
    def _payment_fields(self, order, ui_paymentline):
        res = super()._payment_fields(order, ui_paymentline)
        res["operating_unit_id"] = order.operating_unit_id.id
        return res

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for rec in self:
            if (
                rec.company_id
                and rec.operating_unit_id
                and rec.company_id != rec.operating_unit_id.company_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Company in the POS Order "
                        "and in the Operating Unit must be the same."
                    )
                )
