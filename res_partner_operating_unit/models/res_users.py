# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2020 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, models
from odoo.exceptions import UserError


class ResUsers(models.Model):
    _inherit = "res.users"

    @api.model
    def create(self, vals):
        res = super().create(vals)
        res.partner_id.operating_unit_ids = [(4, res.default_operating_unit_id.id)]
        res.check_partner_operating_unit()
        return res

    def write(self, vals):
        for user in self:
            res = super().write(vals)
            if vals.get("default_operating_unit_id"):
                # Add the new OU
                user.partner_id.operating_unit_ids = [
                    (4, user.default_operating_unit_id.id)
                ]
                user.check_partner_operating_unit()
            return res

    def check_partner_operating_unit(self):
        if (
            self.partner_id.operating_unit_ids
            and self.default_operating_unit_id.id
            not in self.partner_id.operating_unit_ids.ids
        ):
            raise UserError(
                _(
                    "The operating units of the partner must include the default "
                    "one of the user."
                )
            )
