# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock account moves with Operating Unit",
    "summary": "Create journal entries in moves between internal locations "
               "with different operating units.",
    "version": "10.0.1.0.0",
    "category": "Generic Modules/Sales & Purchases",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": [
        'stock_operating_unit',
        'account_operating_unit',
        "stock_account"
    ],
    "installable": True,
}
