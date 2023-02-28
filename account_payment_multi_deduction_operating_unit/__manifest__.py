# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Payment Register Multi Diff with Operating Units",
    "version": "15.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Accounting & Finance",
    "depends": [
        "account_payment_multi_deduction",
        "analytic_operating_unit",
        "account_operating_unit",
    ],
    "data": [
        "wizard/account_payment_register_views.xml",
    ],
    "installable": True,
    "development_status": "Alpha",
    "maintainers": ["Saran440"],
}
