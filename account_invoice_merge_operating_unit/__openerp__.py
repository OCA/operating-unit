# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Account Invoice Merge Operating Unit",

    'summary': """Compatibility between operating unit and account invoice
    merge""",
    'author': "Eficent Business and IT Consulting Services, S.L.,"
              "Odoo Community Association (OCA)",
    'website': "http://www.eficent.com",
    'category': 'Finance',
    'version': '7.0.1.0.0',
    'license': 'AGPL-3',
    'depends': [
        'account_invoice_merge',
        'account_operating_unit',
    ],
    'auto_install': True,
}
