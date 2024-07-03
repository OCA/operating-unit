# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


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
        default=lambda self: self._default_operating_unit(),
    )

    default_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Default Operating Unit",
        default=lambda self: self._default_operating_unit(),
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

    @api.model
    def default_get(self, fields):
        vals = super().default_get(fields)
        if (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param("base_setup.default_user_rights", "False")
            == "True"
        ):
            default_user = self.env.ref("base.default_user")
            vals[
                "default_operating_unit_id"
            ] = default_user.default_operating_unit_id.id
            vals["operating_unit_ids"] = [(6, 0, default_user.operating_unit_ids.ids)]
        return vals

    @api.depends("groups_id", "assigned_operating_unit_ids")
    def _compute_operating_unit_ids(self):
        for user in self:
            if user._origin.has_group("operating_unit.group_manager_operating_unit"):
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
        self.env.registry.clear_cache()

    @api.onchange("operating_unit_ids")
    def _onchange_operating_unit_ids(self):
        for record in self:
            if (
                record.default_operating_unit_id
                and record.default_operating_unit_id
                not in record.operating_unit_ids._origin
            ):
                record.default_operating_unit_id = False

    def operating_units(self):
        return self.env.user.operating_unit_ids
