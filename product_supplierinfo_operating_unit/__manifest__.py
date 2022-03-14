# Copyright 2021 Open For Small Business Ltd - Graeme Gellatly, Rujia Liu
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Product Supplierinfo Operating Unit",
    "summary": """
        Operating Unit in Product Supplier Pricelist""",
    "version": "13.0.1.0.1",
    "license": "AGPL-3",
    "author": "Odoo Community Association (OCA), Open For Small Business Ltd",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["sale", "purchase", "stock_operating_unit", "purchase_operating_unit"],
    "data": ["security/product_supplierinfo.xml", "views/product_supplierinfo.xml"],
    "demo": ["data/product_supplierinfo_demo.xml"],
}
