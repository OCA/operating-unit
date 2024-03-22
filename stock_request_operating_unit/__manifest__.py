# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Stock Request Operating Unit",
    "summary": "Introduces Operating Unit (OU) in stock request",
    "version": "14.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Warehouse Management",
    "depends": ["stock_request", "operating_unit"],
    "license": "AGPL-3",
    "data": [
        "security/stock_request_security.xml",
        "views/stock_request_views.xml",
        "views/stock_request_order_views.xml",
    ],
    "installable": True,
}
