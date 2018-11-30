# Copyright 2015-TODAY Eficent
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License: LGPL-3 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Operating Unit",
    "summary": "An operating unit (OU) is an organizational entity part of a "
               "company",
    "version": "12.0.1.1.0",
    "author": "Eficent, "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Generic",
    "depends": ["base"],
    "license": "LGPL-3",
    "data": [
        "security/operating_unit_security.xml",
        "security/ir.model.access.csv",
        "data/operating_unit_data.xml",
        "view/operating_unit_view.xml",
        "view/res_users_view.xml",
    ],
    'demo': [
        "demo/operating_unit_demo.xml"
    ],
    'installable': True,
}
