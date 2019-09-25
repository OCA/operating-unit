# © 2019 Eficent Business and IT Consulting Services S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.addons.account.models.account_payment \
    import account_payment as AccountPaymentOrig

import logging
_logger = logging.getLogger(__name__)


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.depends('journal_id')
    def _compute_operating_unit_id(self):
        for payment in self:
            if payment.journal_id:
                payment.operating_unit_id = \
                    payment.journal_id.operating_unit_id

    operating_unit_id = fields.Many2one(
        'operating.unit', string='Operating Unit',
        domain="[('user_ids', '=', uid)]",
        compute='_compute_operating_unit_id', store=True)

    def _get_counterpart_move_line_vals(self, invoice=False):
        res = super(AccountPayment,
                    self)._get_counterpart_move_line_vals(invoice=invoice)
        if len(invoice) == 1:
            res['operating_unit_id'] = invoice.operating_unit_id.id or False
        else:
            res['operating_unit_id'] = self.operating_unit_id.id or False
        return res

    def _get_liquidity_move_line_vals(self, amount):
        res = super(AccountPayment, self)._get_liquidity_move_line_vals(amount)
        res['operating_unit_id'] = self.journal_id.operating_unit_id.id \
            or False
        return res

    def _get_dst_liquidity_aml_dict_vals(self):
        dst_liquidity_aml_dict = {
            'name': _('Transfer from %s') % self.journal_id.name,
            'account_id':
                self.destination_journal_id.default_credit_account_id.id,
            'currency_id': self.destination_journal_id.currency_id.id,
            'payment_id': self.id,
            'journal_id': self.destination_journal_id.id,
        }

        dst_liquidity_aml_dict.update({
            'operating_unit_id':
                self.destination_journal_id.operating_unit_id.id or False})
        return dst_liquidity_aml_dict

    def _get_transfer_debit_aml_dict_vals(self):
        transfer_debit_aml_dict = {
            'name': self.name,
            'payment_id': self.id,
            'account_id': self.company_id.transfer_account_id.id,
            'journal_id': self.destination_journal_id.id
        }
        if self.currency_id != self.company_id.currency_id:
            transfer_debit_aml_dict.update({
                'currency_id': self.currency_id.id,
                'amount_currency': -self.amount,
            })
        transfer_debit_aml_dict.update({
            'operating_unit_id':
                self.destination_journal_id.operating_unit_id.id or False
        })
        return transfer_debit_aml_dict

    def _create_transfer_entry(self, amount):
        """ We need to override the standard method, until proper hooks are
        created
        """
        aml_obj = self.env['account.move.line'].with_context(
            check_move_validity=False)
        debit, credit, amount_currency, dummy = aml_obj.with_context(
            date=self.payment_date)._compute_amount_fields(
            amount, self.currency_id, self.company_id.currency_id)
        amount_currency = self.destination_journal_id.currency_id \
            and self.currency_id.with_context(date=self.payment_date).compute(
                amount, self.destination_journal_id.currency_id) or 0

        dst_move = self.env['account.move'].create(
            self._get_move_vals(self.destination_journal_id))

        dst_liquidity_aml_dict = self._get_shared_move_line_vals(
            debit, credit, amount_currency, dst_move.id)
        dst_liquidity_aml_dict.update(self._get_dst_liquidity_aml_dict_vals())
        aml_obj.create(dst_liquidity_aml_dict)

        transfer_debit_aml_dict = self._get_shared_move_line_vals(
            credit, debit, 0, dst_move.id)
        transfer_debit_aml_dict.update(
            self._get_transfer_debit_aml_dict_vals())
        transfer_debit_aml = aml_obj.create(transfer_debit_aml_dict)
        dst_move.post()
        return transfer_debit_aml


    @api.model_cr
    def _register_hook(self):
        super(AccountPayment, self)._register_hook()

        def _create_payment_entry(self, amount):
            """ Create a journal entry corresponding to a payment, if the
                payment references invoice(s) they are reconciled.
                Return the journal entry.
            """
            aml_obj = self.env['account.move.line'].with_context(
                check_move_validity=False)
            debit, credit, amount_currency, currency_id = aml_obj.with_context(
                date=self.payment_date)._compute_amount_fields(
                amount, self.currency_id, self.company_id.currency_id)

            move = self.env['account.move'].create(self._get_move_vals())

            # Write line corresponding to invoice payment
            counterpart_aml_dict = self._get_shared_move_line_vals(
                debit, credit, amount_currency, move.id, False)
            counterpart_aml_dict.update(self._get_counterpart_move_line_vals(
                self.invoice_ids))
            counterpart_aml_dict.update({'currency_id': currency_id})
            counterpart_aml = aml_obj.create(counterpart_aml_dict)

            # Reconcile with the invoices
            if self.payment_difference_handling == 'reconcile' and \
                    self.payment_difference:
                writeoff_line = self._get_shared_move_line_vals(
                    0, 0, 0, move.id, False)
                debit_wo, credit_wo, amount_currency_wo, currency_id = \
                    aml_obj.with_context(date=self.payment_date).\
                        _compute_amount_fields(self.payment_difference,
                                               self.currency_id,
                                               self.company_id.currency_id)
                writeoff_line['name'] = self.writeoff_label
                writeoff_line['account_id'] = self.writeoff_account_id.id
                writeoff_line['debit'] = debit_wo
                writeoff_line['credit'] = credit_wo
                writeoff_line['amount_currency'] = amount_currency_wo
                writeoff_line['currency_id'] = currency_id
                writeoff_line['operating_unit_id'] = \
                    counterpart_aml_dict['operating_unit_id']
                writeoff_line = aml_obj.create(writeoff_line)
                if (counterpart_aml['debit'] or (writeoff_line['credit']
                   and not counterpart_aml['credit'])):
                    counterpart_aml['debit'] += credit_wo - debit_wo
                if (counterpart_aml['credit'] or (writeoff_line['debit']
                   and not counterpart_aml['debit'])):
                    counterpart_aml['credit'] += debit_wo - credit_wo
                counterpart_aml['amount_currency'] -= amount_currency_wo

            # Write counterpart lines
            if not self.currency_id.is_zero(self.amount):
                if not self.currency_id != self.company_id.currency_id:
                    amount_currency = 0
                liquidity_aml_dict = self._get_shared_move_line_vals(
                    credit, debit, -amount_currency, move.id, False)
                liquidity_aml_dict.update(
                    self._get_liquidity_move_line_vals(-amount))
                aml_obj.create(liquidity_aml_dict)

            # validate the payment
            if not self.journal_id.post_at_bank_rec:
                move.post()

            #r econcile the invoice receivable/payable line(s) with the payment
            if self.invoice_ids:
                self.invoice_ids.register_payment(counterpart_aml)

            return move

        origin = getattr(
            AccountPaymentOrig._create_payment_entry, 'origin', None)
        if origin != _create_payment_entry:
            AccountPaymentOrig._patch_method(
                '_create_payment_entry', _create_payment_entry)
            _logger.info('AccountPayment._create_payment_entry method'
                         ' patched to consider operating units!')
