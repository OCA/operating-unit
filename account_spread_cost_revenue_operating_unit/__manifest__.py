# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Cost-Revenue Spread with Operating Units",
    "summary": "This module adds operating unit information to cost-revenue spreads.",
    "version": "15.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Accounting & Finance",
    "depends": ["account_operating_unit", "account_spread_cost_revenue"],
    "license": "AGPL-3",
    "data": [
        "security/account_spread_cost_revenue_security.xml",
        "views/account_spread_views.xml",
    ],
    "installable": True,
    "development_status": "Alpha",
    "maintainers": ["ps-tubtim"],
}
