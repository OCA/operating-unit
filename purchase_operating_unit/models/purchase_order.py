# Copyright 2015-17 ForgeFlow S.L.
# - Jordi Ballester Alomar
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    READONLY_STATES = {
        "purchase": [("readonly", True)],
        "done": [("readonly", True)],
        "cancel": [("readonly", True)],
    }

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        states=READONLY_STATES,
        default=lambda self: (
            self.env["res.users"].operating_unit_default_get(self.env.uid)
        ),
    )

    requesting_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Requesting Operating Unit",
        states=READONLY_STATES,
        default=lambda self: (
            self.env["res.users"].operating_unit_default_get(self.env.uid)
        ),
    )

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
                        "Configuration error. The Company in the Purchase Order "
                        "and in the Operating Unit must be the same."
                    )
                )

    def _prepare_invoice(self):
        invoice_vals = super()._prepare_invoice()
        invoice_vals["operating_unit_id"] = self.operating_unit_id.id
        return invoice_vals


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    operating_unit_id = fields.Many2one(
        related="order_id.operating_unit_id", string="Operating Unit"
    )
