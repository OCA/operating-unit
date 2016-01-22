# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import UserError


class ResCompany(models.Model):
    _inherit = 'res.company'

    inter_ou_clearing_account_id = fields.Many2one('account.account',
                                                   'Inter-operating unit\
                                                   clearing account')

    ou_is_self_balanced = fields.Boolean('Operating Units are self-balanced',
                help="Activate if your company is required to generate a "
                     "balanced balance sheet for each operating unit.",
                     default=True)

    @api.one
    @api.constrains('ou_is_self_balanced')
    def _inter_ou_clearing_acc_required(self):
        if self.ou_is_self_balanced and not \
                self.inter_ou_clearing_account_id:
            raise UserError(_('Configuration error!\nPlease indicate an\
            Inter-operating unit clearing account.'))
