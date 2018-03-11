# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'MIS Builder with Operating Unit',
    'version': '10.0.1.0.0',
    'category': 'Reporting',
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "ACSONE SA/NV,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    'website': 'http://www.eficent.com',
    'depends': ['mis_builder', 'account_operating_unit'],
    'data': [
        'view/mis_builder.xml',
        'security/mis_builder_security.xml'
    ],
    'installable': True,
}
