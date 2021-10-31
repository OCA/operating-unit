# © 2020 Jarsa Sistemas, SA de CV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    def _update_moveline_operating_unit(self, payments, payment, reconciled_moves):
        self.ensure_one()
        destination_account = payments.destination_account_id
        line = payment.move_id.line_ids.filtered(
            lambda l: l.account_id == destination_account
        )
        if payment.move_id.company_id.ou_is_self_balanced:
            to_reconcile = self.env["account.move.line"]
            to_reconcile |= payment.move_id.line_ids.filtered(
                lambda l: l.account_id == destination_account
            )
            to_reconcile |= reconciled_moves.line_ids.filtered(
                lambda l: l.account_id == destination_account
            )
            payment.action_draft()
            line.write(
                {
                    "operating_unit_id": reconciled_moves.operating_unit_id.id,
                }
            )
            payment.action_post()
            to_reconcile.reconcile()
        else:
            line.write(
                {
                    "operating_unit_id": reconciled_moves.operating_unit_id.id,
                }
            )

    def _create_payments(self):
        payments = super()._create_payments()
        if self.group_payment and len(payments) > 1:
            return payments
        for payment in payments:
            reconciled_moves = (
                payment.reconciled_bill_ids + payment.reconciled_invoice_ids
            )
            if reconciled_moves.operating_unit_id != payment.operating_unit_id:
                self._update_moveline_operating_unit(
                    payments, payment, reconciled_moves
                )
        return payments
