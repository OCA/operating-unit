# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2015 Eficent (<http://www.eficent.com/>)
#              <contact@eficent.com>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import fields, models, api


class ResUsers(models.Model):

    _inherit = 'res.users'

    @api.model
    def operating_unit_default_get(self, uid2):
        if not uid2:
            uid2 = self._uid
        user = self.env['res.users'].browse(uid2)
        return user.default_operating_unit_id and \
            user.default_operating_unit_id.id

    @api.model
    def _operating_unit_default_get(self):
        return self.operating_unit_default_get(self._uid)

    @api.model
    def _get_operating_units(self):
        op_unit = self.operating_unit_default_get(self._uid)
        if op_unit:
            return [op_unit]
        return False

    operating_unit_ids = fields.Many2many(
            'operating.unit', 'operating_unit_users_rel',
            'user_id', 'poid', 'Operating Units',
            default=_get_operating_units)
    default_operating_unit_id = fields.Many2one(
            'operating.unit', 'Default Operating Unit',
            default=_operating_unit_default_get)
