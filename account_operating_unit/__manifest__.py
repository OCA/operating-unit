# -*- coding: utf-8 -*-
# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": 'Accounting with Operating Units',
    "summary": "Introduces Operating Unit fields in invoices and "
               "Accounting Entries with clearing account",
    "version": "10.0.1.1.0",
    "author": "Eficent, "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Accounting & Finance",
    "depends": ['account', 'operating_unit', 'analytic_operating_unit'],
    "license": "LGPL-3",
    "data": [
        "security/account_security.xml",
        "views/account_move_view.xml",
        "views/account_journal_view.xml",
        "views/company_view.xml",
        "views/invoice_view.xml",
        "views/account_payment_view.xml",
        "views/account_invoice_report_view.xml",
        "views/report_financial.xml",
        "views/report_trialbalance.xml",
        "views/report_agedpartnerbalance.xml",
        "wizard/account_report_common_view.xml",
        "wizard/account_financial_report_view.xml",
        "wizard/account_report_trial_balance_view.xml",
    ],
    'installable': True,
}
