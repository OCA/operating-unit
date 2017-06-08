# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Purchase Request Qweb Report With Operating Unit',
    'version': '9.0.1.0.0',
    'category': 'Reports/Qweb',
    'license': 'AGPL-3',
    'author': 'Eficent Business and IT Consulting Services S.L., '
              'Serpent Consulting Services Pvt. Ltd.,'
              'Odoo Community Association (OCA)',
    'website': 'https://odoo-community.org/',
    'depends': ['purchase_request_operating_unit',
                'report_qweb_operating_unit'],
    'data': [
        'views/report_purchase_request_qweb.xml',
    ],
    'installable': True,
}
