# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    @api.model
    def _get_batch_available_journals(self, batch_result):
        """Filter available journals by the operating unit of the invoices."""
        journals = super()._get_batch_available_journals(batch_result)
        lines = batch_result.get("lines")
        if lines:
            invoice_ous = lines.move_id.operating_unit_id
            if invoice_ous and len(invoice_ous) == 1:
                journals = journals.filtered(
                    lambda j: not j.operating_unit_id
                    or j.operating_unit_id == invoice_ous
                )
        return journals
