# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in POS",
    "summary": "Adds the concept of operating unit (OU) in POS" "management",
    "version": "15.0.1.0.0",
    "author": "Jarsa," "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Point of Sale",
    "depends": [
        "point_of_sale",
        "stock_account_operating_unit",
    ],
    "license": "LGPL-3",
    "data": [
        "security/pos_security.xml",
        "views/pos_order_view.xml",
        "views/pos_config_view.xml",
        "views/pos_session_view.xml",
        "views/pos_payment_view.xml",
        "views/report_pos_order_view.xml",
    ],
    "demo": [],
    "installable": True,
}
