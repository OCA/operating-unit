# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Analytic Operating Unit",
    "version": "12.0.1.0.0",
    "author": "Eficent, "
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Sales",
    "depends": [
        "analytic",
        "operating_unit",
    ],
    "data": [
        "security/analytic_account_security.xml",
        "views/analytic_account_view.xml",
    ],
    'installable': True,
}
