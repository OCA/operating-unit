# Copyright 2016-19 Eficent Business and IT Consulting Services S.L.
# Copyright 2016-19 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Stock Landed Cost Operating Unit",
    "version": "13.0.1.0.0",
    "license": "LGPL-3",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Generic Modules/Human Resources",
    "depends": ["stock_landed_costs", "account_operating_unit"],
    "data": [
        "views/stock_landed_cost_view.xml",
        "security/stock_landed_cost_security.xml",
    ],
    "installable": True,
}
