# -*- coding: utf-8 -*-
# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class AccountPartialReconcile(models.Model):
    _inherit = 'account.partial.reconcile'

    bal_move_id = fields.Many2one(
        'account.move', index=True)

    @api.multi
    def reverse_bal_entries(self):
        res = False
        for rec in self:
            res = rec.bal_move_id.reverse_moves()
        return res

    @api.multi
    def create_ou_balance(self):
        self.ensure_one()
        ml_obj = self.env['account.move.line']
        if not self.credit_move_id.company_id.ou_is_self_balanced\
                and self.debit_move_id.company_id.ou_is_self_balanced:
            return False

        # If all move lines point to the same operating unit, there's no
        # need to create a balancing move line
        ou_list_ids = [self.credit_move_id.operating_unit_id.id,
                       self.debit_move_id.operating_unit_id.id]
        if ou_list_ids.count(ou_list_ids[0]) == len(ou_list_ids):
            return False

        # Create balancing entries for un-balanced OU's.
        amls = []
        move_id = False
        for ou_id in ou_list_ids:
            # Create a balancing move line in the operating unit
            # clearing account
            if self.credit_move_id.operating_unit_id.id == ou_id:
                if not move_id:
                    move_id = self.env['account.move'].create(
                        self.credit_move_id._get_move_vals())
                line_data = self.credit_move_id.\
                    _prepare_inter_ou_balancing_partial_reconcile(
                        move_id, ou_id, 0.0, self.amount)
            else:
                if not move_id:
                    move_id = self.env['account.move'].create(
                        self.debit_move_id._get_move_vals())
                line_data = self.debit_move_id.\
                    _prepare_inter_ou_balancing_partial_reconcile(
                        move_id, ou_id, self.amount, 0.0)
            amls.append(ml_obj.with_context(wip=True).
                        create(line_data))
        move_id.with_context(wip=False).\
            write({'line_ids': [(4, aml.id) for aml in amls]})
        move_id.with_context(reconciling=True).post()
        return move_id.id

    @api.multi
    def assign_balance_to_partial_reconcile(self):
        if self.env.context.get('reversal', False):
            return
        for rec in self:
            if rec.bal_move_id:
                rec.reverse_bal_entries()
            if rec.debit_move_id.operating_unit_id != \
                    rec.credit_move_id.operating_unit_id:
                rec.bal_move_id = rec.create_ou_balance()

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.bal_move_id and not self.env.context.get('reversal', False):
                rec.with_context(reversal=True).reverse_bal_entries()
        result = super(AccountPartialReconcile, self).unlink()
        return result
