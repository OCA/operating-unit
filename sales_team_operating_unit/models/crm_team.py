# Copyright 2016-17 ForgeFlow S.L. (http://www.forgeflow.com)
# Copyright 2017-TODAY Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        default=lambda self: self.env["res.users"]._get_default_operating_unit(),
        check_company=True,
    )
