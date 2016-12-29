# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Jarsa Sistemas S.A. de C.V..
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, models


class AccountBankStatementLine(models.Model):
    _inherit = 'account.bank.statement.line'

    @api.v7
    def process_reconciliations(self, cr, uid, ids, data, context=None):
        aml_obj = self.pool.get('account.move.line')
        for data_line in data:
            for counterpart in data_line['counterpart_aml_dicts']:
                counterpart_id = counterpart['counterpart_aml_id']
                move_line = aml_obj.browse(cr, uid, counterpart_id, context)
                counterpart['operating_unit_id'] = (
                    move_line.operating_unit_id.id)
        return super(AccountBankStatementLine, self).process_reconciliations(
            cr, uid, ids, data, context=None)
