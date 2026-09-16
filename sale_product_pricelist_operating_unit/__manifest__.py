# Copyright 2025 Camptocamp
# License: LGPL-3 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Sale Product Pricelist Operating Unit",
    "version": "17.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Sales/Sales",
    "depends": [
        # OCA/operating-unit
        "product_pricelist_operating_unit",
        "sale_operating_unit",
    ],
    "data": ["views/sale_order_view.xml"],
    "installable": True,
}
