# -*- coding: utf-8 -*-
# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2016-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "HR Expense Operating Unit",
    "version": "10.0.1.0.0",
    "license": 'LGPL-3',
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Generic Modules/Human Resources",
    "depends": ["hr_expense", "account_operating_unit"],
    "data": [
        "views/hr_expense_view.xml",
        "security/hr_expense_security.xml"
    ],
    'installable': True,
}
