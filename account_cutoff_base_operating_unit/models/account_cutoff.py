# -*- coding: utf-8 -*-
# © 2013-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 Magnus (Willem Hulshof <w.hulshof@magnus.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountCutoff(models.Model):
    _inherit = 'account.cutoff'


    def _get_merge_keys(self):
        """ Return merge criteria for provision lines

        The returned list must contain valid field names
        for account.move.line. Provision lines with the
        same values for these fields will be merged.
        The list must at least contain account_id.
        """
        return ['account_id', 'analytic_account_id', 'operating_unit_id']

    @api.multi
    def _prepare_move(self, to_provision):
        self.ensure_one()
        movelines_to_create = []
        amount_total = 0
        move_label = self.move_label
        merge_keys = self._get_merge_keys()
        key_ou = {}
        for merge_values, amount in to_provision.items():
            vals = {
                'name': move_label,
                'debit': amount < 0 and amount * -1 or 0,
                'credit': amount >= 0 and amount or 0,
            }
            for k, v in zip(merge_keys, merge_values):
                vals[k] = v
                if k == 'operating_unit_id':
                    ou = str(v)
                    if ou not in key_ou:
                        key_ou[ou] = amount
                    else:
                        key_ou[ou] += amount
            movelines_to_create.append((0, 0, vals))

        # add counter-part
        for key, value in key_ou.items():
            counterpart_amount = value * -1

            try:
                movelines_to_create.append((0, 0, {
                    'account_id': self.cutoff_account_id.id,
                    'name': move_label,
                    'debit': counterpart_amount < 0 and counterpart_amount * -1 or 0,
                    'credit': counterpart_amount >= 0 and counterpart_amount or 0,
                    'analytic_account_id': False,
                    'operating_unit_id': int(key)
                }))
            except:
                movelines_to_create.append((0, 0, {
                'account_id': self.cutoff_account_id.id,
                'name': move_label,
                'debit': counterpart_amount < 0 and counterpart_amount * -1 or 0,
                'credit': counterpart_amount >= 0 and counterpart_amount or 0,
                'analytic_account_id': False,}))

        res = {
            'journal_id': self.cutoff_journal_id.id,
            'date': self.cutoff_date,
            'ref': move_label,
            'line_ids': movelines_to_create,
            }
        return res

    @api.multi
    def _prepare_provision_line(self, cutoff_line):
        """ Convert a cutoff line to elements of a move line

        The returned dictionary must at least contain 'account_id'
        and 'amount' (< 0 means debit).

        If you override this, the added fields must also be
        added in an override of _get_merge_keys.
        Adding operating_unit_id.
        """
        res = super(AccountCutoff, self)._prepare_provision_line(cutoff_line)
        if cutoff_line.operating_unit_id:
            res['operating_unit_id'] = cutoff_line.operating_unit_id.id
        return res

    @api.multi
    def _prepare_provision_tax_line(self, cutoff_tax_line):
        """ Convert a cutoff tax line to elements of a move line

        See _prepare_provision_line for more info.
        """
        res = super(AccountCutoff, self)._prepare_provision_tax_line(cutoff_tax_line)
        if cutoff_tax_line.operating_unit_id:
            res['operating_unit_id'] = cutoff_tax_line.operating_unit_id.id
        return res

class AccountCutoffLine(models.Model):
    _inherit = 'account.cutoff.line'

    operating_unit_id = fields.Many2one(
        'operating.unit', 'Operating Unit', readonly=True)


class AccountCutoffTaxLine(models.Model):
    _inherit = 'account.cutoff.tax.line'

    operating_unit_id = fields.Many2one(
        'operating.unit', 'Operating Unit', readonly=True)



