# -*- coding: utf-8 -*-
# © 2017 Genweb2 Limited - Matiar Rahman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class HREmployee(models.Model):

    _inherit = 'hr.employee'

    @api.model
    def _get_operating_unit(self):
        user = self.env['res.users'].browse(self._uid)
        return user.default_operating_unit_id

    @api.model
    def _get_operating_units(self):
        return self._get_operating_unit()

    company_id = fields.Many2one('res.company', string='Company',
                                 default=lambda self: self.env.user.company_id)

    operating_unit_ids = fields.Many2many('operating.unit',
                                          'operating_unit_emp_rel',
                                          'emp_id', 'ou_id', 'Operating Units',
                                          default=_get_operating_units)
