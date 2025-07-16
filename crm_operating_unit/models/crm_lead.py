# © 2015-19 ForgeFlow S.L. - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class CRMLead(models.Model):

    _inherit = "crm.lead"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        related="team_id.operating_unit_id",
    )
