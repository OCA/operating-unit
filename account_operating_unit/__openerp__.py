# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2016 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": 'Accounting with Operating Units',
    "summary": "Introduces Operating Unit fields in invoices and "
               "Accounting Entries with clearing account",
    "version": "9.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Accounting & Finance",
    "depends": ['account', 'operating_unit'],
    "license": "LGPL-3",
    "data": [
        "security/account_security.xml",
        "views/account_move_view.xml",
        "views/account_account_view.xml",
        "views/company_view.xml",
        "views/invoice_view.xml",
        "views/account_invoice_report_view.xml",
        "views/report_financial.xml",
        "wizard/account_report_common_view.xml",
        "wizard/account_financial_report_view.xml",
    ],
    "installable": True,
}
