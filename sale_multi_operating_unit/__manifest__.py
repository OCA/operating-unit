# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).lgpl.html).
{
    "name": "Sale with Multiple Operating Unit",
    "summary": """
        This module allows a user in an operating unit to request internal
        quote to another operating unit.
    """,
    "version": "12.0.1.0.0",
    "author": "Open Source Integrators, "
              "Serpent Consulting Services Pvt. Ltd., "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Sales Management",
    "depends": ["sale_operating_unit", "product_operating_unit",
                "res_partner_operating_unit", "crm"],
    "license": "AGPL-3",
    "data": [
        "views/sale_order_view.xml",
    ],
    'installable': True,
    'development_status': 'Beta',
    'maintainers': [
        'max3903',
    ],
}
