# Copyright 2021 Rujia Liu
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Supplierinfo Operating Unit",
    "summary": """
        Operating Unit in Product Supplier Pricelist""",
    "version": "14.0.1.0.0",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["purchase", "stock_operating_unit"],
    "data": [
        "security/product_supplierinfo.xml",
        "views/product_supplierinfo.xml",
    ],
    "demo": [],
}
