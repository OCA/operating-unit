# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    employee_ids = fields.Many2many(
        comodel_name="hr.employee",
        relation="operating_unit_employees_rel",
        column1="operating_unit_id",
        column2="employee_id",
        string="Employees Allowed",
    )
