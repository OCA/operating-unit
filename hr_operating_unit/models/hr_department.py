# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Department(models.Model):
    _inherit = "hr.department"
    _check_company_auto = True

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=lambda self: (self.env["res.users"].operating_unit_default_get()),
        check_company=True,
    )
