# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2017-TODAY Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Sales Team Operating Unit",
    "version": "12.0.1.1.0",
    "author": "Eficent, "
              "SerpentCS,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Sales",
    "depends": ["sales_team", "operating_unit"],
    "data": [
        "security/crm_security.xml",
        "views/crm_team_view.xml",
    ],
    'installable': True,
}
