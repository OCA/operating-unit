# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock with Operating Units",
    "summary": "An operating unit (OU) is an organizational entity part of a\
        company",
    "version": "9.0.1.0.0",
    "category": "Generic Modules/Sales & Purchases",
    "author": "Eficent, Serpent Consulting Services Pvt. Ltd., "
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "depends": ["stock", "account_operating_unit"],
    "data": [
        "security/stock_security.xml",
        "data/stock_data.xml",
        "view/stock.xml",
    ],
    "demo": [
        "demo/stock_demo.xml",
    ],
    "installable": True,
}
