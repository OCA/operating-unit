# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# Copyright (C) 2019 Open Source Integrators
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models
from odoo.exceptions import UserError
from odoo.fields import Command


class ResUsers(models.Model):
    _inherit = "res.users"

    def _sync_partner_default_operating_unit(self):
        for user in self:
            if user.default_operating_unit_id:
                user.partner_id.operating_unit_ids = [
                    Command.link(user.default_operating_unit_id.id)
                ]
                user.check_partner_operating_unit()

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        for user in users:
            user._sync_partner_default_operating_unit()
        return users

    def write(self, vals):
        res = super().write(vals)
        if vals.get("default_operating_unit_id"):
            for user in self:
                user._sync_partner_default_operating_unit()
        return res

    def check_partner_operating_unit(self):
        for user in self:
            if (
                user.partner_id.operating_unit_ids
                and user.default_operating_unit_id
                and user.default_operating_unit_id.id
                not in user.partner_id.operating_unit_ids.ids
            ):
                raise UserError(
                    self.env._(
                        "The operating units of the partner must include the default "
                        "one of the user."
                    )
                )
