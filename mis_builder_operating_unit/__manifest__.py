# © 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'MIS Builder with Operating Unit',
    'version': '12.0.1.0.0',
    'category': 'Reporting',
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "ACSONE SA/NV,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    'website': 'https://github.com/operating-unit',
    'depends': ['mis_builder', 'account_operating_unit'],
    'data': [
        'security/mis_builder_security.xml',
        'view/mis_builder.xml'
    ],
    'installable': True,
}
