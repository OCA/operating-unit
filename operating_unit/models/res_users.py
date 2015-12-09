# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
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
