# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "HR Expense Sequence by Operating Unit",
    "version": "13.0.1.0.0",
    "license": "LGPL-3",
    "category": "Purchase",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["hr_expense_operating_unit"],
    "data": ["views/operating_unit_view.xml", "views/hr_expense_view.xml"],
    "installable": True,
    "post_init_hook": "assign_ou_sequences",
}
