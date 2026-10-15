# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.fields import Domain


class ResUsers(models.Model):
    _inherit = "res.users"

    operating_unit_ids = fields.One2many(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_ids",
        inverse="_inverse_operating_unit_ids",
        string="Allowed Operating Units",
        compute_sudo=True,
    )

    assigned_operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_users_rel",
        column1="user_id",
        column2="operating_unit_id",
        string="Operating Units",
        default=lambda self: self._get_new_user_operating_units()[0],
    )

    default_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        default=lambda self: self._get_new_user_operating_units()[1],
        domain="[('company_id', '=', current_company_id)]",
    )

    @api.model
    def _get_default_operating_unit(self, uid2=False):
        if not uid2:
            uid2 = self.env.user.id
        user = self.env["res.users"].browse(uid2)
        # check if the company of the default OU is active
        if user.default_operating_unit_id.sudo().company_id in self.env.companies:
            return user.default_operating_unit_id
        else:
            # find an OU of the main active company
            for ou in user.assigned_operating_unit_ids:
                if ou.sudo().company_id in self.env.company:
                    return ou
            # find an OU of any active company
            for ou in user.assigned_operating_unit_ids:
                if ou.sudo().company_id in self.env.companies:
                    return ou
        return False

    @api.model
    def _default_operating_unit(self):
        return self._get_default_operating_unit()

    @api.depends("group_ids", "assigned_operating_unit_ids")
    @api.depends_context("allowed_company_ids")
    def _compute_operating_unit_ids(self):
        if self.env.context.get("allowed_company_ids"):
            dom = Domain.OR(
                [
                    Domain("company_id", "=", False),
                    Domain("company_id", "in", self.env.context["allowed_company_ids"]),
                ]
            )
        else:
            dom = Domain.TRUE
        for user in self:
            if user.has_group("operating_unit.group_manager_operating_unit"):
                user.operating_unit_ids = self.env["operating.unit"].search(dom)
            else:
                user.operating_unit_ids = (
                    user.assigned_operating_unit_ids.filtered_domain(dom)
                )

    @api.model
    def _get_new_user_operating_units(self, company=None):
        """(allowed OUs, default OU) for a new user: company defaults if set,
        else the OU of the creating user."""
        company = (company or self.env.company).sudo()
        default_ou = company.new_user_default_operating_unit_id
        if company.new_user_operating_unit_ids or default_ou:
            return company.new_user_operating_unit_ids | default_ou, default_ou
        default_ou = self._default_operating_unit() or self.env["operating.unit"]
        return default_ou, default_ou

    @api.model_create_multi
    def create(self, vals_list):
        ou_fields = {
            "assigned_operating_unit_ids",
            "operating_unit_ids",
            "default_operating_unit_id",
        }
        for vals in vals_list:
            # field defaults use env.company, not the company of the new user
            if vals.get("company_id") and ou_fields.isdisjoint(vals):
                allowed, default = self._get_new_user_operating_units(
                    self.env["res.company"].browse(vals["company_id"])
                )
                vals["assigned_operating_unit_ids"] = [fields.Command.set(allowed.ids)]
                vals["default_operating_unit_id"] = default.id
        return super().create(vals_list)

    @api.onchange("company_id")
    def _onchange_company_id_operating_units(self):
        for user in self.filtered(lambda u: not u._origin and u.company_id):
            allowed, default = self._get_new_user_operating_units(user.company_id)
            user.operating_unit_ids = allowed
            user.default_operating_unit_id = default

    def _inverse_operating_unit_ids(self):
        for user in self:
            user.assigned_operating_unit_ids = user.operating_unit_ids

    @api.onchange("operating_unit_ids")
    def _onchange_operating_unit_ids(self):
        for record in self:
            if (
                record.default_operating_unit_id
                and record.default_operating_unit_id
                not in record.operating_unit_ids._origin
            ):
                record.default_operating_unit_id = False

    def _get_invalidation_fields(self):
        return super()._get_invalidation_fields() | {
            "assigned_operating_unit_ids",
            "default_operating_unit_id",
        }

    def operating_units(self):
        return self.env.user.operating_unit_ids
