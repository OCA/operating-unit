# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HrEmployeeBase(models.AbstractModel):
    _inherit = "hr.employee.base"

    operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="operating_unit_employees_rel",
        column1="employee_id",
        column2="operating_unit_id",
        string="Operating Units",
        default=lambda self: (self.env["res.users"].operating_unit_default_get()),
    )

    default_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Default Operating Unit",
        default=lambda self: (self.env["res.users"].operating_unit_default_get()),
    )
