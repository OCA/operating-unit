# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SurveyQuestionInherit(models.Model):
    _inherit = "survey.question"

    operating_unit_id = fields.Many2one(
        related="survey_id.operating_unit_id",
        store=True,
    )

    @api.constrains("operating_unit_id")
    def _check_operating_unit_change(self):
        for question in self:
            if (
                question.id
                and question.operating_unit_id != question.survey_id.operating_unit_id
            ):
                raise ValidationError(_("Changing the Operating Unit is not allowed."))
