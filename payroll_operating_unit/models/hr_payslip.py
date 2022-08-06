# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        default=lambda s: s.env["res.users"].operating_unit_default_get(s._uid),
    )

    @api.onchange("contract_id")
    def onchange_contract(self):
        for rec in self:
            ou = False
            if rec.contract_id and rec.contract_id.operating_unit_id:
                ou = rec.contract_id.operating_unit_id
            elif rec.employee_id and rec.employee_id.default_operating_unit_id:
                ou = rec.employee_id.default_operating_unit_id
            rec.operating_unit_id = ou

    @api.onchange("employee_id", "date_from", "date_to", "struct_id")
    def onchange_employee(self):

        res = super().onchange_employee()
        self.onchange_contract()

        return res
