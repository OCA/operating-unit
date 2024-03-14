# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Accounting with Operating Units",
    "summary": "Introduces Operating Unit (OU) in invoices and "
    "Accounting Entries with clearing account",
    "version": "16.0.1.0.0",
    "author": "ForgeFlow, "
    "Serpent Consulting Services Pvt. Ltd.,"
    "WilldooIT Pty Ltd,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Accounting & Finance",
    "depends": [
        "account",
        "analytic_operating_unit",
        "base_view_inheritance_extension",
    ],
    "license": "LGPL-3",
    "data": [
        "security/account_security.xml",
        "views/account_move_view.xml",
        "views/account_journal_view.xml",
        "views/company_view.xml",
        "views/account_payment_view.xml",
        "views/account_invoice_report_view.xml",
    ],
}
