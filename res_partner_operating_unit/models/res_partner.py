# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2020 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError
from odoo.osv import expression


class ResPartner(models.Model):
    _inherit = "res.partner"
    _check_company_auto = True

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "operating_unit_partner_rel",
        "partner_id",
        "operating_unit_id",
        "Operating Units",
        compute="_compute_operating_unit_ids",
        readonly=False,
        store=True,
    )

    @api.depends("user_ids.assigned_operating_unit_ids")
    def _compute_operating_unit_ids(self):
        for partner in self:
            if partner.user_ids:
                partner.operating_unit_ids = (
                    partner.user_ids.assigned_operating_unit_ids
                )

    @api.constrains("operating_unit_ids")
    def _check_operating_unit_ids(self):
        for partner in self:
            if partner.user_ids:
                expected = partner.user_ids.mapped("assigned_operating_unit_ids")
                if partner.operating_unit_ids != expected:
                    raise UserError(
                        _(
                            "Operating units on a partner linked to a user must match "
                            "the user's operating units. "
                            "Please update the operating units "
                            "on the related user(s) instead."
                        )
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
        domain = expression.AND([self._user_ous_domain(), domain])
        return super().search(domain, offset=offset, limit=limit, order=order)

    @api.model
    def search_count(self, domain, limit=None):
        domain = expression.AND([self._user_ous_domain(), domain])
        return super().search_count(domain, limit=limit)
