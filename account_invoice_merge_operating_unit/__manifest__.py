# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': "Account Invoice Merge Operating Unit",
    'author': "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    'website': "http://www.eficent.com",
    'category': 'Finance',
    'version': '10.0.1.0.0',
    'license': 'LGPL-3',
    'depends': [
        'account_invoice_merge',
        'account_operating_unit',
    ],
    'data': [
        'wizard/invoice_merge_view.xml',
    ],
    'auto_install': True,
}
