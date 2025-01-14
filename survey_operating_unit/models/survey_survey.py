# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class SurveySurveyInherit(models.Model):
    _inherit = "survey.survey"

    def _default_operating_unit(self):
        if (
            self.env.user.default_operating_unit_id.sudo().company_id
            in self.env.companies
        ):
            return self.env.user.default_operating_unit_id
        else:
            # find an OU of the main active company
            for ou in self.env.user.assigned_operating_unit_ids:
                if ou.sudo().company_id in self.env.company:
                    return ou
            # find an OU of any active company
            for ou in self.env.user.assigned_operating_unit_ids:
                if ou.sudo().company_id in self.env.companies:
                    return ou

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=lambda self: self._default_operating_unit(),
    )
