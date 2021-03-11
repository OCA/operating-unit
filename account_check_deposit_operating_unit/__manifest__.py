# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Operating Unit in Check Deposit",
    "version": "13.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Accounting",
    "depends": ["account_check_deposit", "account_operating_unit"],
    "data": ["security/check_deposit_security.xml", "views/check_deposit_views.xml"],
    "maintainers": ["newtratip"],
    "installable": True,
}
