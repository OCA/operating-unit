# -*- coding: utf-8 -*-
# © 2009 EduSense BV (<http://www.edusense.nl>)
# © 2011-2013 Therp BV (<http://therp.nl>)
# © 2016 Serv. Tecnol. Avanzados - Pedro M. Baeza
# © 2016 Akretion (Alexis de Lattre - alexis.delattre@akretion.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountPaymentOrder(models.Model):
    _inherit = 'account.payment.order'


    company_id = fields.Many2one(
        related='payment_mode_id.company_id', store=True, readonly=True)
    operating_unit_id = fields.Many2one(
        related='journal_id.operating_unit_id', store=True, readonly=True)
    journal_id = fields.Many2one(
        'account.journal', string='Bank Journal', ondelete='restrict',
        readonly=True, states={'draft': [('readonly', False)]},
        track_visibility='onchange')


    @api.multi
    def _prepare_move_line_offsetting_account(self, amount_company_currency, amount_payment_currency, bank_lines):
        vals = super(AccountPaymentOrder, self)._prepare_move_line_offsetting_account(
                                    amount_company_currency, amount_payment_currency, bank_lines)
        vals['operating_unit_id'] = self.journal_id.operating_unit_id.id
        return vals

    @api.multi
    def _prepare_move_line_partner_account(self, bank_line):
        vals = super(AccountPaymentOrder, self)._prepare_move_line_partner_account(bank_line)
        if bank_line.payment_line_ids[0].move_line_id:
            vals['operating_unit_id'] = bank_line.payment_line_ids[0].move_line_id.operating_unit_id.id
        else:
            vals['operating_unit_id'] = self.journal_id.operating_unit_id.id
        return vals

