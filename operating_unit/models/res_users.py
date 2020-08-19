# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ResUsers(models.Model):

    _inherit = "res.users"

    @api.model
    def operating_unit_default_get(self, uid2=False):
        if not uid2:
            uid2 = self._uid
        user = self.env["res.users"].browse(uid2)
        return user.default_operating_unit_id

    @api.model
    def _default_operating_unit(self):
        return self.operating_unit_default_get()

    @api.model
    def _default_operating_units(self):
        return self._default_operating_unit()

    operating_unit_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_ids",
        inverse="_inverse_operating_unit_ids",
    )
    assigned_operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_users_rel",
        column1="user_id",
        column2="operating_unit_id",
        string="Operating Units",
        default=lambda self: self._default_operating_units(),
    )

    default_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Default Operating Unit",
        default=lambda self: self._default_operating_unit(),
    )

    @api.depends("groups_id", "assigned_operating_unit_ids")
    def _compute_operating_unit_ids(self):
        for user in self:
            if user.has_group("operating_unit.group_manager_operating_unit"):
                dom = []
                if self.env.context.get("allowed_company_ids"):
                    dom = [
                        "|",
                        ("company_id", "=", False),
                        ("company_id", "in", self.env.context["allowed_company_ids"]),
                    ]
                else:
                    dom = []
                user.operating_unit_ids = self.env["operating.unit"].sudo().search(dom)
            else:
                user.operating_unit_ids = user.assigned_operating_unit_ids

    def _inverse_operating_unit_ids(self):
        for user in self:
            user.assigned_operating_unit_ids = user.operating_unit_ids
