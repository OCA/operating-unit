# -*- coding: utf-8 -*-
# © 2013-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 Magnus (Willem Hulshof <w.hulshof@magnus.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Cut-off Base Operating Unit',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'OU adaptation for Base module Account Cut-offs',
    'author': 'Magnus,Odoo Community Association (OCA)',
    'website': 'http://www.magnus.nl',
    'depends': ['account_operating_unit',
                'account_cutoff_base',
                'account_cutoff_prepaid'],
    'data': ['views/account_cutoff.xml',
    ],
    'installable': True,
}
