# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class HrAttendance(models.Model):
    _inherit = "hr.attendance"

    operating_unit_id = fields.Many2one(
        'operating.unit', 'Operating Unit',
        default=lambda self: self.env['res.users'].operating_unit_default_get()
    )

    @api.model
    def create(self, values):
        if self.env.user.id == 1:
            # On kiosk logged user is __system__
            employee = self.env['hr.employee'].browse(
                [values['employee_id'], ])
            values['operating_unit_id'] = employee.default_operating_unit_id.id
        record = super().create(values)
        return record
