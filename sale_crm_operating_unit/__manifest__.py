# Copyright 2015-19 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Sale CRM Operating Unit",
    "version": "11.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Sales",
    "depends": [
        "sale_crm",
        "crm_operating_unit",
        "sale_operating_unit",
        "base_view_inheritance_extension",
    ],
    "data": [
        'views/sale_crm_view.xml'
    ],
    "license": "LGPL-3",
    'installable': True,
}
