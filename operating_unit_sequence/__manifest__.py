# Copyright 2020 Sunflower IT <https://www.sunflowerweb.nl>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'Operating Unit Sequence',
    'version': '12.0.1.0.0',
    'category': 'Operating Unit',
    'author': 'Sunflower IT, Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'website': 'http://www.sunflowerweb.in',
    'depends': [
        'base',
        'operating_unit'
    ],
    'data': [
        'views/operating_unit.xml',
        'views/ir_sequence.xml'
    ],
    'installable': True,
}
