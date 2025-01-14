# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SurveyUserInputInherit(models.Model):
    _inherit = "survey.user_input"

    operating_unit_id = fields.Many2one(
        related="survey_id.operating_unit_id",
        store=True,
    )

    @api.constrains("operating_unit_id")
    def _check_operating_unit_change(self):
        for user_input in self:
            if (
                user_input.id
                and user_input.operating_unit_id
                != user_input.survey_id.operating_unit_id
            ):
                raise ValidationError(_("Changing the Operating Unit is not allowed."))
