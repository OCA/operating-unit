# -*- coding: utf-8 -*-
# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _


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
        compute='_compute_operating_unit_id', readonly=True, store=True)

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

        if self.currency_id != self.company_id.currency_id:
            dst_liquidity_aml_dict.update({
                'currency_id': self.currency_id.id,
                'amount_currency': self.amount,
            })

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
                self.journal_id.operating_unit_id.id or False
        })
        return transfer_debit_aml_dict

    def _create_transfer_entry(self, amount):
        """ We need to override the standard method, until proper hooks are
        created
        """
        aml_obj = self.env['account.move.line'].with_context(
            check_move_validity=False)
        debit, credit, amount_currency, dummy = aml_obj.with_context(
            date=self.payment_date).compute_amount_fields(
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
