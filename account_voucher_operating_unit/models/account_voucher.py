# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class AccountVoucher(models.Model):
    _inherit = "account.voucher"

    @api.multi
    def _get_default_operating_unit(self):
        journal = self._default_journal()
        if isinstance(journal, int):
            journal = self.env['account.journal'].browse(journal)
        ttype = self.env.context.get('voucher_type', False)
        if ttype in ('sale', 'purchase'):
            return journal.default_debit_account_id.operating_unit_id.id

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        default=_get_default_operating_unit,
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if rec.company_id and rec.operating_unit_id and \
                    rec.company_id != rec.operating_unit_id.company_id:
                raise ValidationError(_('The Company in the Move Line and in '
                                        'the Operating Unit must be the same.'
                                        ))

    @api.multi
    @api.constrains('operating_unit_id', 'journal_id', 'voucher_type')
    def _check_journal_account_operating_unit(self):
        for rec in self:
            if rec.voucher_type not in ('purchase', 'sale'):
                return True
            if (
                rec.journal_id and rec.operating_unit_id and
                rec.journal_id.default_debit_account_id and
                rec.journal_id.default_debit_account_id.operating_unit_id and
                rec.journal_id.default_debit_account_id.operating_unit_id.id !=
                    rec.operating_unit_id.id
            ) or (
                rec.journal_id and rec.operating_unit_id and
                rec.journal_id.default_credit_account_id and
                rec.journal_id.default_credit_account_id.operating_unit_id and
                rec.journal_id.default_credit_account_id.operating_unit_id.id !=
                    rec.operating_unit_id.id
            ):
                raise ValidationError(_('The Default Debit and Credit Accounts'
                                        ' defined in the Journal must have the'
                                        ' same Operating Unit as the one '
                                        'indicated in the payment or receipt.'
                                        ))
        return True

    @api.multi
    def first_move_line_get(self, move_id, company_currency, current_currency):
        self.ensure_one()
        res = super(AccountVoucher, self).first_move_line_get(
            move_id, company_currency, current_currency)
        voucher = self
        if not voucher.operating_unit_id:
            return res
        if voucher.voucher_type == 'purchase':
            if voucher.account_id.operating_unit_id:
                res['operating_unit_id'] = \
                    voucher.account_id.operating_unit_id.id
            else:
                raise ValidationError(_('Account %s - %s does not have a '
                                'default operating unit. \n '
                                'Journal %s default Debit and '
                                'Credit accounts should have a '
                                'default Operating Unit.') %
                              (voucher.account_id.code,
                               voucher.account_id.name,
                               voucher.journal_id.name))
        else:
            if voucher.operating_unit_id:
                res['operating_unit_id'] = voucher.operating_unit_id.id
            else:
                raise ValidationError(_('The Voucher must have an Operating '
                                'Unit.'))
        return res




class AccountVoucherLine(models.Model):
    _inherit = "account.voucher.line"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        related='voucher_id.operating_unit_id',
        string='Operating Unit', readonly=True,
        store=True,
    )

    @api.model
    def create(self, vals):
        if not 'operating_unit_id' in vals:
            voucher= self.env['account.voucher'].browse(vals['voucher_id'])
            if voucher.operating_unit_id:
                vals['operating_unit_id'] = voucher.operating_unit_id.id
        return super(AccountVoucherLine, self).create(vals)
