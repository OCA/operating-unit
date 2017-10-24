# -*- coding: utf-8 -*-
# © 2017 Genweb2 Limited - Matiar Rahman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class HREmployee(models.Model):

    _inherit = 'hr.employee'

    @api.model
    def operating_unit_default_get(self, uid2):
        if not uid2:
            uid2 = self._uid
        user = self.env['res.users'].browse(uid2)
        return user.default_operating_unit_id

    @api.model
    def _get_operating_unit(self):
        return self.operating_unit_default_get(self._uid)

    @api.model
    def _get_operating_units(self):
        return self._get_operating_unit()

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id)

    operating_unit_ids = fields.Many2many('operating.unit',
                                          'operating_unit_emp_rel',
                                          'emp_id', 'ou_id', 'Operating Units',
                                          default=_get_operating_units)

    @api.onchange('user_id')
    def _onchange_user(self):
        super(HREmployee, self)._onchange_user()
        if self.user_id:

            if self.operating_unit_ids:
                ou_ids = self.operating_unit_ids.ids
            else:
                ou_ids = []

            if self.user_id.default_operating_unit_id.id not in ou_ids:
                ou_ids.append(self.user_id.default_operating_unit_id.id)

            self.operating_unit_ids = [(6, 0, ou_ids)]
