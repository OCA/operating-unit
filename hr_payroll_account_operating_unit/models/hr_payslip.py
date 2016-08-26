# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.tools.translate import _
from openerp import models, fields, api
from openerp.exceptions import Warning


class HrPayslip(models.Model):

    _inherit = 'hr.payslip'

    @api.multi
    def write(self, vals):
        res = super(HrPayslip, self).write(vals)
        if 'move_id' in vals and vals['move_id']:
            for slip in self:
                if slip.contract_id and slip.contract_id.operating_unit_id:
                    slip.move_id.write({'operating_unit_id':
                                        slip.contract_id.operating_unit_id.id})
        return res

    @api.cr_uid_ids_context
    def process_sheet(self, cr, uid, ids, context=None):
        OU = None
        payslip = self.browse(cr, uid, ids, context=context)
        for slip in payslip:
            # Check that all slips are related to contracts
            # that belong to the same OU.
            if OU:
                if slip.contract_id.operating_unit_id.id != OU:
                    raise Warning(_('Configuration error!\nThe Contracts must\
                    refer the same Operating Unit.'))
            OU = slip.contract_id.operating_unit_id.id
        # Add to context the OU of the employee contract
        new_context = context.copy()
        new_context.update(force_operating_unit=OU)
        return super(HrPayslip, self).process_sheet(cr, uid, payslip.ids,
                                                    new_context)
