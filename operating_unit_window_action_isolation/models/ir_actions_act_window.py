# Copyright (C) 2016-2027 CIT Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models
from odoo.osv import expression
from odoo.tools.safe_eval import safe_eval


class IrActionsActWindow(models.Model):
    _inherit = "ir.actions.act_window"

    def read(self, fields=None, load="_classic_read"):
        """Restrict actions to the user's default operating unit."""
        result = super().read(fields=fields, load=load)

        if self.env.is_superuser():
            return result

        user_ou = self.env.user.default_operating_unit_id
        if not user_ou:
            return result

        for action in result:
            res_model = action.get("res_model")

            if (
                not res_model
                or res_model not in self.env
                or "operating_unit_id"
                not in self.env[res_model]._fields
            ):
                continue

            ou_domain = [
                ("operating_unit_id", "in", [False, user_ou.id])
            ]

            domain = []
            if action.get("domain"):
                try:
                    domain = safe_eval(action["domain"])
                except (ValueError, SyntaxError, TypeError):
                    continue

            action["domain"] = expression.AND(
                [domain, ou_domain]
            )

        return result
