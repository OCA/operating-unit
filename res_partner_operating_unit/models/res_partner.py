# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2020 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _check_company_auto = True

    @api.model
    def _default_operating_unit(self):
        user = self.env["res.users"].browse(self.env.user.id)
        return user.default_operating_unit_id

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "operating_unit_partner_rel",
        "partner_id",
        "operating_unit_id",
        "Operating Units",
        required=True,
        default=lambda self: self._default_operating_unit(),
    )
