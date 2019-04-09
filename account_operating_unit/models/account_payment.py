# -*- coding: utf-8 -*-
# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


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

    def _get_shared_move_line_vals(
            self, debit, credit, amount_currency, move_id, invoice_id=False):
        res = super(AccountPayment, self)._get_shared_move_line_vals(
            debit, credit, amount_currency, move_id, invoice_id)
        res.update(operating_unit_id=self.operating_unit_id.id)
        return res
