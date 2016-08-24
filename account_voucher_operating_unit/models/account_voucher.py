# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import Warning


class AccountVoucher(models.Model):
    _inherit = "account.voucher"

    @api.multi
    def _get_default_operating_unit(self):
        journal = self._get_journal()
        if isinstance(journal, int):
            journal = self.env['account.journal'].browse(journal)
        ttype = self.env.context.get('type', False)
        if ttype in ('payment', 'receipt'):
            return journal.default_debit_account_id.operating_unit_id.id

    @api.multi
    def onchange_journal(self, journal_id, line_ids, tax_id,
                         partner_id, date, amount, ttype, company_id):
        res = super(AccountVoucher, self).onchange_journal(
            journal_id, line_ids, tax_id, partner_id, date, amount, ttype,
            company_id)
        if journal_id and ttype in ('payment', 'receipt'):
            journal = self.env['account.journal'].browse(journal_id)
            res['value']['operating_unit_id'] = \
                journal.default_debit_account_id.operating_unit_id.id
            res['value']['writeoff_operating_unit_id'] = \
                journal.default_debit_account_id.operating_unit_id.id
        return res

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        default=_get_default_operating_unit,
    )
    writeoff_operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Write-off Operating Unit',
        default=_get_default_operating_unit,
        required=False,
    )

    @api.one
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        if self.company_id and self.operating_unit_id and \
                self.company_id != self.operating_unit_id.company_id:
            raise Warning(_('The Company in the Move Line and in the '
                            'Operating Unit must be the same.'))

    @api.one
    @api.constrains('operating_unit_id', 'journal_id', 'type')
    def _check_journal_account_operating_unit(self):
        if self.type not in ('payment', 'receipt'):
            return True
        if (
            self.journal_id and self.operating_unit_id and
            self.journal_id.default_debit_account_id and
            self.journal_id.default_debit_account_id.operating_unit_id and
            self.journal_id.default_debit_account_id.operating_unit_id.id !=
                self.operating_unit_id.id
        ) or (
            self.journal_id and self.operating_unit_id and
            self.journal_id.default_credit_account_id and
            self.journal_id.default_credit_account_id.operating_unit_id and
            self.journal_id.default_credit_account_id.operating_unit_id.id !=
                self.operating_unit_id.id
        ):
            raise Warning(_('The Default Debit and Credit Accounts '
                            'defined in the Journal must have the same '
                            'Operating Unit as the one indicated in the '
                            'payment or receipt.'))
        return True

    @api.model
    def first_move_line_get(self, voucher_id, move_id,
                            company_currency, current_currency):
        res = super(AccountVoucher, self).first_move_line_get(
            voucher_id, move_id, company_currency, current_currency)
        voucher = self.env['account.voucher'].browse(voucher_id)
        if not voucher.operating_unit_id:
            return res
        if voucher.type in ('payment', 'receipt'):
            if voucher.account_id.operating_unit_id:
                res['operating_unit_id'] = \
                    voucher.account_id.operating_unit_id.id
            else:
                raise Warning(_('Account %s - %s does not have a '
                                'default operating unit. \n '
                                'Payment Method %s default Debit and '
                                'Credit accounts should have a '
                                'default Operating Unit.') %
                              (voucher.account_id.code,
                               voucher.account_id.name,
                               voucher.journal_id.name))
        else:
            if voucher.operating_unit_id:
                res['operating_unit_id'] = voucher.operating_unit_id.id
            else:
                raise Warning(_('The Voucher must have an Operating '
                                'Unit.'))
        return res

    @api.model
    def _voucher_move_line_prepare(self, voucher_id, line_total,
                                   move_id, company_currency, current_currency,
                                   voucher_line_id, ):
        res = super(AccountVoucher, self)._voucher_move_line_prepare(
            voucher_id, line_total, move_id, company_currency,
            current_currency, voucher_line_id)
        line = self.env['account.voucher.line'].browse(voucher_line_id)

        if line.voucher_id.type in ('sale', 'purchase') \
                and line.voucher_id.operating_unit_id:
            res['operating_unit_id'] = line.voucher_id.operating_unit_id.id
        elif line.move_line_id and line.move_line_id.operating_unit_id:
            res['operating_unit_id'] = line.move_line_id.operating_unit_id.id
        return res

    @api.model
    def _voucher_move_line_foreign_currency_prepare(
            self, voucher_id, line_total, move_id,
            company_currency, current_currency, voucher_line_id,
            foreign_currency_diff):

        res = super(AccountVoucher, self)._voucher_move_line_prepare(
            voucher_id, line_total, move_id, company_currency,
            current_currency, voucher_line_id, foreign_currency_diff)
        line = self.env['account.voucher.line'].browse(voucher_line_id)
        if line.move_line_id and line.move_line_id.operating_unit_id:
            res['operating_unit_id'] = line.move_line_id.operating_unit_id.id
        return res

    @api.model
    def writeoff_move_line_get(self, voucher_id,
                               line_total, move_id, name,
                               company_currency, current_currency):
        res = super(AccountVoucher, self).writeoff_move_line_get(
            voucher_id, line_total, move_id, name, company_currency,
            current_currency)
        if res:
            voucher = self.env['account.voucher'].browse(voucher_id)
            if (voucher.payment_option == 'with_writeoff' or
                    voucher.partner_id):
                if not voucher.writeoff_operating_unit_id:
                    raise Warning(_('Please indicate a write-off Operating '
                                    'Unit.'))
                else:
                    res['operating_unit_id'] = \
                        voucher.writeoff_operating_unit_id.id
            else:
                if not voucher.writeoff_operating_unit_id:
                    if not voucher.account_id.operating_unit_id:
                        raise Warning(_('Please indicate a write-off '
                                        'Operating Unit or a default '
                                        'Operating Unit for account %s') %
                                      voucher.account_id.code)
                    else:
                        res['operating_unit_id'] = \
                            voucher.account_id.operating_unit_id.id
                else:
                        res['operating_unit_id'] = \
                            voucher.writeoff_operating_unit_id.id
        return res


class AccountVoucherLine(models.Model):
    _inherit = "account.voucher.line"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        related='voucher_id.operating_unit_id',
        string='Operating Unit', readonly=True,
        store=True,
    )
