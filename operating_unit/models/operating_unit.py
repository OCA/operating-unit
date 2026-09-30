# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class OperatingUnit(models.Model):
    _name = "operating.unit"
    _description = "Operating Unit"
    _rec_names_search = ["name", "code"]

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    user_ids = fields.Many2many(
        "res.users",
        "operating_unit_users_rel",
        "operating_unit_id",
        "user_id",
        "Users Allowed",
    )

    _sql_constraints = [
        (
            "code_company_uniq",
            "unique (code,company_id)",
            "The code of the operating unit must " "be unique per company!",
        ),
        (
            "name_company_uniq",
            "unique (name,company_id)",
            "The name of the operating unit must " "be unique per company!",
        ),
    ]

    @api.depends("name", "code")
    def _compute_display_name(self):
        for ou in self:
            ou.display_name = f"[{ou.code}] {ou.name}"

    @api.model_create_multi
    def create(self, vals_list):
        res = super().create(vals_list)
        res.write({"user_ids": [fields.Command.link(self.env.user.id)]})
        self.env.registry.clear_cache()
        return res

    def write(self, vals):
        self.env.registry.clear_cache()
        return super().write(vals)

    def button_open_linked_users(self):
        self.ensure_one()
        action = self.env.ref(
            "base.action_res_users",
            raise_if_not_found=False,
        )
        if not action:
            return False
        action_vals = action.read()[0]

        user_ids = set(self.user_ids.ids)
        group = self.env.ref(
            "operating_unit.group_manager_operating_unit",
            raise_if_not_found=False,
        )
        if group:
            user_ids.update(group.users.ids)

        user_ids = list(user_ids)

        context = action_vals.get("context", {})
        if isinstance(context, str):
            from odoo.tools.safe_eval import safe_eval

            context = safe_eval(context)

        context.update(
            {
                "create": False,
                "edit": False,
                "delete": False,
            }
        )
        action_vals["context"] = context

        if not user_ids:
            return action_vals

        action_vals["domain"] = [("id", "in", user_ids)]
        if len(user_ids) == 1:
            form_view = self.env.ref("base.view_users_form")
            action_vals.update(
                {
                    "views": [(form_view.id, "form")],
                    "view_mode": "form",
                    "res_id": user_ids[0],
                }
            )
        else:
            action_vals.update(
                {
                    "views": [(False, "list"), (False, "form")],
                    "view_mode": "list,form",
                }
            )
        return action_vals
