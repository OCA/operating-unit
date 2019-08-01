##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

{
    'name': 'Operating Unit in Contacts and Contact Tags',
    'summary': 'Adds the concept of operating unit (OU) in contacts '
               'and contact tags',
    'version': '12.0.1.0.0',
    'author': 'brain-tec AG, '
              'Odoo Community Association (OCA)',
    'website': 'https://github.com/OCA/operating-unit',
    'category': 'Sales Management',
    'depends': [
        'base',
        'operating_unit',
    ],
    'license': 'LGPL-3',
    'data': [
        'security/res_partner_category_security.xml',
        'security/res_partner_security.xml',

        'views/res_partner_category_view.xml',
        'views/res_partner_view.xml',
    ],
    'installable': True,
}
