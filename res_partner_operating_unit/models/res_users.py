# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2020 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import Command, _, api, models
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model_create_multi
    def create(self, vals_list):
        users = super().create(vals_list)
        for user in users:
            user_ou = user.default_operating_unit_id or user._default_operating_unit()
            user.partner_id.operating_unit_ids = [Command.link(user_ou.id)]
            user.check_partner_operating_unit()
        return users

    def write(self, vals):
        for user in self:
            res = super().write(vals)
            if vals.get("default_operating_unit_id"):
                # Add the new OU
                user.partner_id.operating_unit_ids = [
                    Command.link(user.default_operating_unit_id.id)
                ]
                user.check_partner_operating_unit()
            return res

    def check_partner_operating_unit(self):
        self.ensure_one()
        if (
            self.partner_id.operating_unit_ids
            and self.default_operating_unit_id
            and (
                self.default_operating_unit_id.id
                not in self.partner_id.operating_unit_ids.ids
            )
        ):
            raise UserError(
                _(
                    "The operating units of the partner must include the default "
                    "one of the user."
                )
            )
