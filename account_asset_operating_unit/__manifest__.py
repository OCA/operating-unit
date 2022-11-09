# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Asset with Operating Units",
    "summary": "This module adds operating unit information to assets.",
    "version": "14.0.1.0.1",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Accounting & Finance",
    "depends": ["account_operating_unit", "account_asset_management"],
    "license": "AGPL-3",
    "data": [
        "security/account_asset_security.xml",
        "views/account_asset_views.xml",
        "wizard/wiz_account_asset_report.xml",
    ],
    "installable": True,
    "development_status": "Alpha",
    "maintainers": ["ps-tubtim"],
}
