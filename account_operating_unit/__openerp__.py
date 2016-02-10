# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": 'Accounting with Operating Units',
    "summary": "An operating unit (OU) is an organizational entity part of a\
        company",
    "version": "8.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Generic/Sales & Purchases",
    "depends": ['account', 'operating_unit'],
    "license": "AGPL-3",
    "data": [
        "security/account_security.xml",
        "views/account_move_view.xml",
        "views/account_account_view.xml",
        "views/company_view.xml",
        "views/invoice_view.xml",
        "wizard/account_report_common_view.xml",
        "wizard/account_financial_report_view.xml",
    ],
    "installable": True,
}
