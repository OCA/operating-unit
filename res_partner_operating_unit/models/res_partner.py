# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2020 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"
    _check_company_auto = True

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "operating_unit_partner_rel",
        "partner_id",
        "operating_unit_id",
        "Operating Units",
    )

    # Extending methods to replace a record rule.
    # Ref: https://github.com/OCA/operating-unit/issues/258
    @api.model
    def _user_ous_domain(self):
        ou_ids = self.env.user.operating_unit_ids.ids
        return [
            "|",
            ("operating_unit_ids", "in", ou_ids),
            ("operating_unit_ids", "=", False),
        ]

    @api.model
    def search(self, domain, offset=0, limit=None, order=None):
        domain = self._user_ous_domain() + domain
        return super().search(domain, offset=offset, limit=limit, order=order)

    @api.model
    def search_count(self, domain, limit=None):
        domain = self._user_ous_domain() + domain
        return super().search_count(domain, limit=limit)
