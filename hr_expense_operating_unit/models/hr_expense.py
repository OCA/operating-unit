# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models


class HrExpenseExpense(models.Model):

    _inherit = 'hr.expense'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))

    @api.multi
    def action_move_create(self):
        res = super(HrExpenseExpense, self).action_move_create()
        self.account_move_id.write({'operating_unit_id':
                                    self.operating_unit_id.id})
        return res
