# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "HR Payroll Account Operating Unit",
    "version": "9.0.1.0.0",
    "license": 'AGPL-3',
    "author": "Eficent",
    "category": "Generic Modules/Human Resources",
    "depends": ["hr_payroll_account", "hr_contract_operating_unit", "account_operating_unit"],
    "description": """
HR Payroll Account Operating Unit
=================================
Adds a the operating unit to the account moves created by the payslip,
based on the employee's Operating Unit defined in the Contract.
    """,
    'installable': True,
}
