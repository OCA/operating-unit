# Copyright 2016-19 ForgeFlow S.L.
# Copyright 2016-19 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrExpenseExpense(models.Model):

    _inherit = "hr.expense"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for rec in self:
            if (
                rec.company_id
                and rec.operating_unit_id
                and rec.company_id != rec.operating_unit_id.company_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Company in "
                        "the Expense and in the Operating "
                        "Unit must be the same."
                    )
                )

    @api.constrains("operating_unit_id", "sheet_id")
    def _check_expense_operating_unit(self):
        for rec in self:
            if (
                rec.sheet_id
                and rec.sheet_id.operating_unit_id
                and rec.operating_unit_id
                and rec.sheet_id.operating_unit_id != rec.operating_unit_id
            ):
                raise ValidationError(
                    _(
                        "Configuration error. The Operating "
                        "Unit in the Expense sheet and in the "
                        "Expense must be the same."
                    )
                )

    def _create_sheet_from_expenses(self):
        sheet = super()._create_sheet_from_expenses()
        if len(self.mapped("operating_unit_id")) != 1 or any(
            not expense.operating_unit_id for expense in self
        ):
            raise ValidationError(
                _(
                    "You cannot submit the Expenses having "
                    "different Operating Units or with "
                    "no Operating Unit"
                )
            )
        sheet.write({"operating_unit_id": self.mapped("operating_unit_id").id})
        return sheet

    def _get_account_move_line_values(self):
        res = super(HrExpenseExpense, self)._get_account_move_line_values()
        for expense in self:
            res[expense.id][0].update({"operating_unit_id": self.operating_unit_id.id})
            res[expense.id][1].update({"operating_unit_id": self.operating_unit_id.id})
        return res


class HrExpenseSheet(models.Model):

    _inherit = "hr.expense.sheet"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )

    @api.onchange("operating_unit_id")
    def _onchange_operating_unit_id(self):
        if self.operating_unit_id:
            self.expense_line_ids.write(
                {"operating_unit_id": self.operating_unit_id.id}
            )

    @api.constrains("operating_unit_id", "company_id")
    def _check_company_operating_unit(self):
        for rec in self:
            if (
                rec.company_id
                and rec.operating_unit_id
                and rec.company_id != rec.operating_unit_id.company_id
            ):
                raise ValidationError(
                    _(
                        """Configuration error. The company in
                the Expense and in the Operating Unit must be the same"""
                    )
                )
