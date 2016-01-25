# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L. (www.eficent.com)
# - Jordi Ballester Alomar
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import fields, models


class AccountAccount(models.Model):
    _inherit = "account.account"

    operating_unit_id = fields.Many2one('operating.unit',
                                        'Default Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))
