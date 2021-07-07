# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "operating_unit_employees_rel",
        "employee_id",
        "operating_unit_id",
        "Operating Units",
        default=lambda self: (self.env["res.users"].operating_unit_default_get()),
    )

    default_operating_unit_id = fields.Many2one(
        "operating.unit",
        "Default Operating Unit",
        default=lambda self: (self.env["res.users"].operating_unit_default_get()),
    )
