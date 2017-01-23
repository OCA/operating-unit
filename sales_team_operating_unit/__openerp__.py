# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Sales Team Operating Unit",
    "version": "9.0.1.0.0",
    "author": "Eficent, "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "http://www.eficent.com",
    "category": "Sales",
    "depends": ["sales_team", "operating_unit"],
    "data": [
        "views/crm_team_view.xml",
        "security/crm_security.xml",
    ],
    'installable': True,
}
