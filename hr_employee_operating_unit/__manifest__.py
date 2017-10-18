# -*- coding: utf-8 -*-
# © 2017 Genweb2 Limited - Matiar Rahman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Employee Operating Unit",
    "author": "Matiar Rahman, "
              "Genweb2 Limited,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Human Resources",
    "depends": ["hr", "operating_unit"],
    "data": [
        "views/hr_views.xml",
        "security/security.xml",
    ],

    'installable': True,
    'application': False,
}
