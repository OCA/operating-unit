# -*- coding: utf-8 -*-
# © 2015-17 Eficent
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Vouchers with Operating Units',
    'summary': 'Introduces the operating unit to vouchers',
    'version': '10.0.1.0.0',
    'category': 'Generic Modules/Sales & Purchases',
    "author": "Eficent, "
              "Ecosoft Co. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    'website': 'http://www.eficent.com',
    'depends': ['account_operating_unit', 'account_voucher'],
    'data': [
        'views/account_voucher_sales_purchase_view.xml',
        'security/account_voucher_security.xml'
    ],
    'installable': True,
}
