# © 2019 Eficent Business and IT Consulting Services S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from .import test_account_operating_unit as test_ou
import time


class TestInvoiceOperatingUnit(test_ou.TestAccountOperatingUnit):

    def test_payment_from_invoice(self):
        """Create and invoice and a subsquent payment, in another OU"""

        # Create invoice for B2B operating unit
        self.invoice = self.invoice_model.sudo(self.user_id.id).create(
            self._prepare_invoice(self.b2b.id))
        # Validate the invoice
        self.invoice.sudo(self.user_id.id).action_invoice_open()

        # Pay the invoice using a cash journal associated to the main company
        ctx = {'active_model': 'account.invoice', 'active_ids': [
            self.invoice.id]}
        register_payments = \
            self.register_payments_model.with_context(ctx).create({
                'payment_date': time.strftime('%Y') + '-07-15',
                'journal_id': self.cash_journal_ou1.id,
                'payment_method_id': self.payment_method_manual_in.id
            })

        register_payments.create_payments()
        payment = self.payment_model.search([], order="id desc", limit=1)

        self.assertAlmostEqual(payment.amount, 115000)
        self.assertEqual(payment.state, 'posted')
        self.assertEqual(self.invoice.state, 'paid')
