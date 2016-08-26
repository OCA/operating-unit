# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, models


class AccountMove(models.Model):

    _inherit = 'account.move'

    @api.model
    def create(self, vals):
        if 'force_operating_unit' in self._context:
            for line in vals['line_ids']:
                line[2].update({'operating_unit_id':
                                self._context['force_operating_unit']})
        return super(AccountMove, self).create(vals)
