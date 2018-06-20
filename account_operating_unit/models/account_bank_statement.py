# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Jarsa Sistemas S.A. de C.V..
# © 2018 Willem Hulshof, Magnus.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    def _prepare_reconciliation_move_line(self, move, amount):
        res = super(AccountBankStatementLine, self)._prepare_reconciliation_move_line(move, amount)
        res['operating_unit_id'] = self.journal_id.operating_unit_id.id
        return res

    @api.multi
    def process_reconciliations(self, data):
        AccountMoveLine = self.env['account.move.line']
        for st_line, datum in zip(self, data):
            for aml_dict in datum.get('counterpart_aml_dicts', []):
                aml_dict['move_line'] = AccountMoveLine.browse(aml_dict['counterpart_aml_id'])
                aml_dict['operating_unit_id'] = aml_dict['move_line'].operating_unit_id.id
        return super(AccountBankStatementLine, self).process_reconciliations(data)

class AccountReconcileModel(models.Model):
    _inherit = "account.reconcile.model"

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit')

    @api.onchange('journal_id')
    def onchange_operating_units(self):
        if self.journal_id:
            self.operating_unit_id = self.journal_id.operating_unit_id and self.journal_id.operating_unit_id.id
        else:
            self.operating_unit_id = False
