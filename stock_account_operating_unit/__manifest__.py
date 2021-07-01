# © 2019 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# Rujia Liu
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock account moves with Operating Unit",
    "summary": "Create journal entries in moves between internal locations "
    "with different operating units.",
    "version": "14.0.1.0.0",
    "category": "Generic Modules/Sales & Purchases",
    "author": "Eficent Business and IT Consulting Services S.L., "
    "Serpent Consulting Services Pvt. Ltd., "
    "O4SB Ltd, "
    "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["stock_operating_unit", "account_operating_unit", "stock_account"],
    "data": [
        "security/stock_account_security.xml",
        "views/stock_valuation_layer_views.xml",
    ],
    "installable": True,
}
