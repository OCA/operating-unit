# Copyright 2020 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ContractContract(models.Model):

    _inherit = "contract.contract"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )

    def _prepare_invoice(self, date_invoice, journal=None):
        (invoice_vals, move_form) = super()._prepare_invoice(
            date_invoice, journal=journal
        )
        if self.operating_unit_id:
            invoice_vals["operating_unit_id"] = self.operating_unit_id.id
        return (invoice_vals, move_form)
