# © 2015-19 ForgeFlow S.L. - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class CRMLead(models.Model):
    _inherit = "crm.lead"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        compute="_compute_operating_unit",
        store=True,
    )

    @api.depends("team_id.operating_unit_id")
    def _compute_operating_unit(self):
        default_team = self.env["crm.team"]._get_default_team_id()
        default_operating_unit = self.env["res.users"]._get_default_operating_unit(
            self._uid
        )
        for record in self:
            team = record.team_id or default_team
            if team.operating_unit_id:
                record.operating_unit_id = team.operating_unit_id
            else:
                record.operating_unit_id = default_operating_unit
