# Copyright 2019 ForgeFlow S.L.
# Copyright 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock with Operating Units",
    "summary": "Adds the concept of operating unit (OU) in stock management",
    "version": "16.0.1.2.1",
    "category": "Generic Modules/Sales & Purchases",
    "author": "ForgeFlow, "
    "Serpent Consulting Services Pvt. Ltd., "
    "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["stock", "operating_unit"],
    "data": ["security/stock_security.xml", "data/stock_data.xml", "view/stock.xml"],
    "demo": ["demo/stock_demo.xml"],
    "installable": True,
}
