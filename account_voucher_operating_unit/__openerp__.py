# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Vouchers with Operating Units',
    'summary': 'Introduces the operating unit to vouchers',
    'version': '9.0.1.0.0',
    'category': 'Generic Modules/Sales & Purchases',
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Ecosoft Co. Ltd.,"
              "Odoo Community Association (OCA)",
    'website': 'http://www.eficent.com',
    'depends': ['account_voucher_move_line_create_hooks',
                'account_operating_unit', 'operating_unit'],
    'data': [
        'views/account_voucher_payment_receipt_view.xml',
        'views/account_voucher_sales_purchase_view.xml',
        'security/account_voucher_security.xml'
    ],
    'installable': True,
}
