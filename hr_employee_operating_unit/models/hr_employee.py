# -*- coding: utf-8 -*-
# © 2017 Genweb2 Limited - Matiar Rahman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models

class HREmployee(models.Model):

    _inherit = 'hr.employee'

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id)

    operating_unit_id = fields.Many2one(
        'operating.unit',
        'Operating Unit',
        default=lambda self: self.env['res.users'].operating_unit_default_get(
            self._uid))

    @api.onchange('user_id')
    def _onchange_user(self):
        super(HREmployee, self)._onchange_user()
        self.operating_unit_id = self.user_id.default_operating_unit_id