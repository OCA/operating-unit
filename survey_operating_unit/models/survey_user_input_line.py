# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SurveyUserInputLineInherit(models.Model):
    _inherit = "survey.user_input.line"

    operating_unit_id = fields.Many2one(
        related="user_input_id.operating_unit_id",
        store=True,
    )

    @api.constrains("operating_unit_id")
    def _check_operating_unit_change(self):
        for line in self:
            if (
                line.id
                and line.operating_unit_id != line.user_input_id.operating_unit_id
            ):
                raise ValidationError(_("Changing the Operating Unit is not allowed."))
