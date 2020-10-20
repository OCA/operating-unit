# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# Copyright (C) 2019 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models, _
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.partner_id.operating_unit_ids = \
            [(4, res.default_operating_unit_id.id)]
        return res

    @api.multi
    def write(self, vals):
        res = super().write(vals)
        if vals.get('default_operating_unit_id'):
            # Add the new OU
            self.partner_id.operating_unit_ids = \
                [(4, vals['default_operating_unit_id'])]
        return res

    @api.constrains('partner_id.operating_unit_ids',
                    'default_operating_unit_id')
    def check_partner_operating_unit(self):
        if self.partner_id.operating_unit_ids and \
                self.default_operating_unit_id.id not in \
                self.partner_id.operating_unit_ids.ids:
            raise UserError(_(
                "The operating units of the partner must include the default "
                "one of the user."))
