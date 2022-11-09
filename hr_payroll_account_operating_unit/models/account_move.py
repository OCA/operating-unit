# Copyright 2016-17 ForgeFlow S.L.
# Copyright 2016-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class AccountMove(models.Model):

    _inherit = "account.move"

    @api.constrains("operating_unit_id")
    def check_payslips_ou(self):
        for move in self:
            pay = self.env["hr.payslip"].sudo().search([("move_id", "=", move.id)])
            if (pay.operating_unit_id and move.operating_unit_id) and (
                pay.operating_unit_id != move.operating_unit_id
            ):
                raise ValidationError(
                    _(
                        "The journal entry and the payslip must have same "
                        "operating unit"
                    )
                )
        return True
