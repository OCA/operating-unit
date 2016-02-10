# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
{
    "name": "Operating Unit in Sales",
    "version": "8.0.1.0.0",
    "summary": "An operating unit (OU) is an organizational entity part of a "
               "company",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "http://www.eficent.com",
    "category": "Sales Management",
    "depends": ["sale", "operating_unit"],
    "data": [
        "views/sale_view.xml",
        "security/sale_security.xml",
    ],
    'installable': True,
    'active': False,
}
