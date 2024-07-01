# Copyright 2024 NSI-SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


from odoo import api, models


class IrRule(models.Model):
    _inherit = "ir.rule"

    @api.model
    def _eval_context(self):
        res = super()._eval_context()
        res.update(
            {
                "operating_unit_ids": self.env.user.operating_units().ids,
                "operating_unit_id": self.env.user.default_operating_unit_id.id,
            }
        )
        return res
