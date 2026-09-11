# Copyright 2025 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Product Pricelist Operating Unit",
    "version": "17.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Product",
    "depends": [
        # Odoo
        "product",
        # OCA/operating-unit
        "operating_unit",
    ],
    "data": ["security/ir_rule.xml", "views/product_pricelist_view.xml"],
    "installable": True,
}
