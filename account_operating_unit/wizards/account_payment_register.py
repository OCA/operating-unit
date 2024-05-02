# © 2020 Jarsa Sistemas, SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, models
from odoo.exceptions import UserError


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _get_reconciled_moves(self, payment):
        return payment.reconciled_bill_ids + payment.reconciled_invoice_ids

    def _create_payments(self):
        payments = super()._create_payments()
        if self.group_payment and len(payments) > 1:
            return payments
        for payment in payments:
            to_reconcile = self.env["account.move.line"]
            reconciled_moves = self._get_reconciled_moves(payment)
            if len(reconciled_moves.operating_unit_id) > 1:
                raise UserError(
                    _(
                        "The OU in the Bills/Invoices to register payment must be the same."
                    )
                )
            if reconciled_moves.operating_unit_id != payment.operating_unit_id:
                destination_account = payment.destination_account_id
                line = payment.move_id.line_ids.filtered(
                    lambda l: l.account_id == destination_account
                )
                line.write(
                    {
                        "operating_unit_id": reconciled_moves.operating_unit_id.id,
                    }
                )
                # reconcile with case self balanced only
                if payment.move_id.company_id.ou_is_self_balanced:
                    to_reconcile |= line
                    to_reconcile |= reconciled_moves.line_ids.filtered(
                        lambda l: l.account_id == destination_account
                    )
                    payment.action_draft()
                    payment.action_post()
                    to_reconcile.filtered(lambda r: not r.reconciled).reconcile()
        return payments
