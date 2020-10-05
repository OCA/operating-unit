# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import time

from . import test_account_operating_unit as test_ou


class TestInvoiceOperatingUnit(test_ou.TestAccountOperatingUnit):
    def test_payment_from_invoice(self):
        """Create and invoice and a subsquent payment, in another OU"""

        # Create invoice for B2B operating unit
        self.invoice = self.move_model.with_user(self.user_id.id).create(
            self._prepare_invoice(self.b2b.id)
        )
        # Validate the invoice
        self.invoice.with_user(self.user_id.id).action_post()

        # Pay the invoice using a cash journal associated to the main company
        ctx = {"active_model": "account.move", "active_ids": [self.invoice.id]}
        register_payments = self.register_payments_model.with_context(ctx).create(
            {
                "payment_date": time.strftime("%Y") + "-07-15",
                "journal_id": self.cash_journal_ou1.id,
                "payment_method_id": self.payment_method_manual_in.id,
            }
        )

        register_payments.create_payments()
        payment = self.payment_model.search([], order="id desc", limit=1)
        # Validate that inter OU balance move lines are created
        self.assertEqual(len(payment.mapped("move_line_ids.move_id.line_ids")), 4)
        self.assertAlmostEqual(payment.amount, 115000)
        self.assertEqual(payment.state, "posted")
        self.assertEqual(self.invoice.invoice_payment_state, "paid")

    def test_payment_from_two_invoices(self):
        """ Create two invoices of different OU and payment from a third OU"""

        # Create invoices for B2B and B2C operating units
        to_create = [
            self._prepare_invoice(self.b2b.id, "SUPP/B2B/01"),
            self._prepare_invoice(self.b2c.id, "SUPP/B2C/02"),
        ]
        invoices = self.move_model.with_user(self.user_id.id).create(to_create)
        # Validate the invoices
        invoices.with_user(self.user_id.id).action_post()

        # Pay the invoices using a cash journal associated to the main company
        ctx = {"active_model": "account.move", "active_ids": invoices.ids}
        register_payments = self.register_payments_model.with_context(ctx).create(
            {
                "payment_date": time.strftime("%Y") + "-07-15",
                "journal_id": self.cash_journal_ou1.id,
                "payment_method_id": self.payment_method_manual_in.id,
            }
        )

        register_payments.create_payments()
        payments = self.payment_model.search([], order="id desc", limit=2)
        for payment in payments:
            # Validate that inter OU balance move lines are created
            self.assertEqual(len(payment.mapped("move_line_ids.move_id.line_ids")), 4)
            self.assertAlmostEqual(payment.amount, 115000)
            self.assertEqual(payment.state, "posted")
            self.assertEqual(payment.invoice_ids.invoice_payment_state, "paid")

    def test_payment_transfer(self):
        """Create a transfer payment with journals in different OU"""

        payment = self.payment_model.create(
            {
                "payment_type": "transfer",
                "amount": 115000,
                "payment_date": time.strftime("%Y") + "-07-15",
                "journal_id": self.cash_journal_ou1.id,
                "destination_journal_id": self.cash2_journal_b2b.id,
                "payment_method_id": self.payment_method_manual_in.id,
            }
        )
        payment.post()
        self.assertEqual(len(payment.move_line_ids.mapped("operating_unit_id")), 2)
        # Validate that every move has their correct OU
        for move in payment.move_line_ids.mapped("move_id"):
            ou_in_lines = move.line_ids.mapped("operating_unit_id")
            self.assertEqual(len(ou_in_lines), 1)
            ou_in_journal = move.journal_id.operating_unit_id
            self.assertEqual(ou_in_lines, ou_in_journal)
