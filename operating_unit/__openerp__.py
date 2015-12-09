# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit",
    "version": "9.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Generic",
    "depends": ["base"],
    "description": """
Operating Unit
==============
An operating unit (OU) is an organizational entity part of a company, with
separate management ownership. Management by OU is aimed to introduce the
following features:

- Partition data from other OU's.
- Define its own sequencing schemes.
- Administer user access to the data for processing and reporting.
- Is not product or customer specific.
- Provides OU specific P&L and Balance sheet

The current module defines the operating unit entity and the user's security
rules. Other modules extend the standard Odoo apps with the OU.
    """,
    "license": "LGPL-3",
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
