# Copyright 2024 NSI-SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class IrRule(models.Model):
    _inherit = "ir.rule"

    @api.model
    def _eval_context(self):
        res = super()._eval_context()
        ou_id = (
            self.env.context.get("current_operating_unit_id")
            or self.env.user.default_operating_unit_id.id
        )
        ou_ids = self.env.user.operating_units().ids
        # When a specific OU is active, restrict the visible set to that OU
        # only — mirrors the company switcher: selected OU determines which
        # records are visible, while ou_ids still represents all allowed OUs
        # for contexts where the full set is needed.
        effective_ou_ids = [ou_id] if ou_id else ou_ids
        res.update(
            {
                "operating_unit_ids": effective_ou_ids,
                "operating_unit_id": ou_id or False,
            }
        )
        return res
