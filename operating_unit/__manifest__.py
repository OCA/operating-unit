# -*- coding: utf-8 -*-
# © 2015-2017 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-2017 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License: AGPL-3 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

{
    "name": "Operating Unit",
    "summary": "An operating unit (OU) is an organizational entity part of a "
               "company",
    "version": "10.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Generic",
    "depends": ["base"],
    "license": "AGPL-3",
    "data": [
        "security/operating_unit_security.xml",
        "security/ir.model.access.csv",
        "view/operating_unit_view.xml",
        "view/res_users_view.xml",
        "data/operating_unit_data.xml",
    ],
    'demo': [
        "demo/operating_unit_demo.xml"
    ],
    'installable': True,
}
