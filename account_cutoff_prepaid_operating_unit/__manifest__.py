# -*- coding: utf-8 -*-
# © 2013-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 Magnus (Willem Hulshof <w.hulshof@magnus.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Account Cut-off Prepaid OU',
    'version': '10.0.1.0.0',
    'category': 'Accounting & Finance',
    'license': 'AGPL-3',
    'summary': 'OU adaptation Prepaid Expense, Prepaid Revenue',
    'author': 'Magnus,Odoo Community Association (OCA)',
    'website': 'http://www.akretion.com',
    'depends': [
        'account_cutoff_prepaid',
        'account_operating_unit',
        'account_cutoff_base_operating_unit',
        ],
    'data': [
#        'views/account_cutoff.xml',
    ],
    'images': [
        ],
    'installable': True,
}
