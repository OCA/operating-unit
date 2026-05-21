# Copyright 2016-17 ForgeFlow S.L. (http://www.forgeflow.com)
# Copyright 2017-TODAY Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        default=lambda self: self.env["res.users"]._get_default_operating_unit(),
        check_company=True,
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        if res.get("operating_unit_id"):
            operating_unit = self.env["operating.unit"].browse(res["operating_unit_id"])
            res["company_id"] = operating_unit.company_id.id
        return res
