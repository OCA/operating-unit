# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "HR Expense Operating Unit",
    "version": "9.0.1.0.0",
    "license": 'LGPL-3',
    "author": "Eficent",
    "category": "Generic Modules/Human Resources",
    "depends": ["hr_expense", "account_operating_unit"],
    "description": """
HR Expense Operating Unit
=========================
Adds a the operating unit to the HR Expense.
    """,
    "data": [
        "views/hr_expense_view.xml",
        "security/hr_expense_security.xml"
    ],
    'installable': True,
}
