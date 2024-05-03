# Copyright 2016-17 ForgeFlow S.L.
# Copyright 2016-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class HrPayslip(models.Model):

    _inherit = "hr.payslip"

    operating_unit_id = fields.Many2one(related="contract_id.operating_unit_id")

    def write(self, vals):
        res = super(HrPayslip, self).write(vals)
        if vals.get("move_id", False):
            for slip in self:
                if slip.operating_unit_id:
                    slip.move_id.operating_unit_id = slip.operating_unit_id.id
                    if slip.move_id.line_ids:
                        slip.move_id.line_ids.write(
                            {"operating_unit_id": slip.operating_unit_id.id}
                        )
        return res

    def _prepare_debit_line(
        self,
        line,
        slip,
        amount,
        date,
        debit_account_id,
        analytic_salary_id,
        tax_ids,
        tax_tag_ids,
        tax_repartition_line_id,
    ):
        res = super()._prepare_debit_line(
            line,
            slip,
            amount,
            date,
            debit_account_id,
            analytic_salary_id,
            tax_ids,
            tax_tag_ids,
            tax_repartition_line_id,
        )
        res.update(operating_unit_id=slip.operating_unit_id.id)
        return res

    def _prepare_credit_line(
        self,
        line,
        slip,
        amount,
        date,
        credit_account_id,
        analytic_salary_id,
        tax_ids,
        tax_tag_ids,
        tax_repartition_line_id,
    ):
        res = super()._prepare_credit_line(
            line,
            slip,
            amount,
            date,
            credit_account_id,
            analytic_salary_id,
            tax_ids,
            tax_tag_ids,
            tax_repartition_line_id,
        )
        res.update(operating_unit_id=slip.operating_unit_id.id)
        return res

    def _prepare_adjust_credit_line(
        self, currency, credit_sum, debit_sum, journal, date
    ):
        res = super()._prepare_adjust_credit_line(
            currency, credit_sum, debit_sum, journal, date
        )
        res.update(operating_unit_id=self.operating_unit_id.id)
        return res

    def _prepare_adjust_debit_line(
        self, currency, credit_sum, debit_sum, journal, date
    ):
        res = super()._prepare_adjust_debit_line(
            currency, credit_sum, debit_sum, journal, date
        )
        res.update(operating_unit_id=self.operating_unit_id.id)
        return res
