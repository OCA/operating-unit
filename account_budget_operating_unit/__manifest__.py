# -*- coding: utf-8 -*-
# © 2015-2017 Eficent
# - Jordi Ballester Alomar
# © 2015-2017 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# © 2015-2017 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Budget with Operating Units',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    "author": "Eficent, "
              "Ecosoft Co. Ltd.,"
              "Serpent CS,"
              "Odoo Community Association (OCA)",
    'website': 'http://www.eficent.com',
    "license": "LGPL-3",
    'depends': ['account_budget', 'operating_unit'],
    'data': [
        'views/account_budget_view.xml',
        'security/account_budget_security.xml'
    ],
    'installable': True,
}
