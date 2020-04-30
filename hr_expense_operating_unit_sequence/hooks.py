from odoo import SUPERUSER_ID, api


def assign_ou_sequences(cr, registry):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        operating_unit_obj = env["operating.unit"]
        sequence_obj = env["ir.sequence"]
        for operating_unit in operating_unit_obj.search([]):
            name_format = "Hr Expense Order of {}"
            hr_exp_seq = sequence_obj.create(
                {
                    "name": name_format.format(operating_unit.name),
                    "code": "hr.expense.{}".format(operating_unit.code),
                    "prefix": "{}-EXP".format(operating_unit.code),
                    "padding": 5,
                    "company_id": operating_unit.company_id.id,
                }
            )
            operating_unit.write({"hr_expense_sequence_id": hr_exp_seq.id})
