# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Accounting Fincnaial Report Operating Unit",
    "summary": "Introduces Operating Unit (OU) in financial reports",
    "version": "15.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Accounting & Finance",
    "depends": ["account_financial_report", "account_operating_unit"],
    "license": "AGPL-3",
    "data": [
        "wizards/aged_partner_balance_wizard_view.xml",
        "wizards/general_ledger_wizard_view.xml",
        "wizards/journal_ledger_wizard_view.xml",
        "wizards/open_items_wizard_view.xml",
        "wizards/trial_balance_wizard_view.xml",
        "wizards/vat_report_wizard_view.xml",
    ],
}
