# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    hr_expense_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="HR Expense Sequence",
        help="Sequence of HR Expense with this operating unit",
    )
