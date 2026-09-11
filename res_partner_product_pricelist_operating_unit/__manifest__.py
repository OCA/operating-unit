# Copyright 2025 Camptocamp
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Partner Product Pricelist Operating Unit",
    "version": "17.0.1.0.0",
    "author": "Camptocamp, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Product",
    "depends": [
        # OCA/operating-unit
        "product_pricelist_operating_unit",
        "res_partner_operating_unit",
    ],
    "data": [
        "views/res_partner.xml",
    ],
    "installable": True,
}
