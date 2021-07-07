# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    employee_ids = fields.Many2many(
        "hr.employee",
        "operating_unit_employees_rel",
        "operating_unit_id",
        "employee_id",
        "Employees Allowed",
    )
