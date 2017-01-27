# -*- coding: utf-8 -*-
# © 2015 Eficent
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class AccountVoucher(models.Model):
    _inherit = "account.voucher"

    @api.multi
    def _get_default_operating_unit(self):
        user = self.env['res.users'].browse(self._uid)
        return user.default_operating_unit_id

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        default=lambda self: self.env['res.users'].operating_unit_default_get(
            self._uid),
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if rec.company_id and rec.operating_unit_id and \
                    rec.company_id != rec.operating_unit_id.company_id:
                raise ValidationError(_('The Company in the voucher and in the'
                                        'Operating Unit must be the same.'
                                        ))

    @api.multi
    def account_move_get(self):
        self.ensure_one()
        move = super(AccountVoucher, self).account_move_get()
        if not self.operating_unit_id:
            return move
        else:
            if self.operating_unit_id:
                move['operating_unit_id'] = self.operating_unit_id.id
            else:
                raise ValidationError(_('The Voucher must have an Operating '
                                        'Unit.'))
        return move

    @api.multi
    def first_move_line_get(self, move_id, company_currency, current_currency):
        self.ensure_one()
        res = super(AccountVoucher, self).first_move_line_get(
            move_id, company_currency, current_currency)
        if not self.operating_unit_id:
            return res
        else:
            if self.operating_unit_id:
                res['operating_unit_id'] = self.operating_unit_id.id
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
        if 'operating_unit_id' not in vals:
            voucher = self.env['account.voucher'].browse(vals['voucher_id'])
            if voucher.operating_unit_id:
                vals['operating_unit_id'] = voucher.operating_unit_id.id
        return super(AccountVoucherLine, self).create(vals)
