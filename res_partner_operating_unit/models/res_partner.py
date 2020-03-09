# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.model
    def operating_unit_default_get(self, uid2=False):
        if not uid2:
            uid2 = self._uid
        user = self.env['res.users'].browse(uid2)
        return user.default_operating_unit_id

    @api.model
    def _default_operating_unit(self):
        return self.operating_unit_default_get()

    @api.model
    def _default_operating_units(self):
        return self._default_operating_unit()

    operating_unit_ids = fields.Many2many(
        'operating.unit', 'operating_unit_partner_rel',
        'partner_id', 'operating_unit_id',
        'Operating Units',
        default=lambda self: self._default_operating_units())

    # Extending methods to replace a record rule.
    # Ref: https://github.com/OCA/operating-unit/issues/258
    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
        # Get the OUs of the user
        ou_ids = self.env.user.operating_unit_ids.ids
        domain = ['|',
                  ('operating_unit_ids', 'in', ou_ids),
                  ('operating_unit_ids', '=', False)]
        return super().search(domain + args, offset=offset, limit=limit,
                              order=order, count=count)

    @api.model
    def search_count(self, args):
        # Get the OUs of the user
        ou_ids = self.env.user.operating_unit_ids.ids
        domain = ['|',
                  ('operating_unit_ids', 'in', ou_ids),
                  ('operating_unit_ids', '=', False)]
        return super().search_count(domain + args)
