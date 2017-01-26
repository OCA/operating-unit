# -*- coding: utf-8 -*-
# © 2015-17 Eficent - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in Procurement Orders",
    "summary": "An operating unit (OU) is an organizational entity part of a "
               "company",
    "version": "10.0.1.0.0",
    "author": "Eficent, Serpent Consulting Services Pvt. Ltd., "
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Stock Management",
    "license": "LGPL-3",
    "depends": ["procurement", "operating_unit", "stock_operating_unit"],
    "data": [
        "security/procurement_security.xml",
    ],
    'installable': True,
}
