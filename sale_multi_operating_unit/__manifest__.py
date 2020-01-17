# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).lgpl.html).
{
    "name": "Sale with Multiple Operating Unit",
    "summary": "Allow a unit to request internal quotes to another",
    "version": "12.0.1.0.0",
    "author": "Open Source Integrators, "
              "Serpent Consulting Services Pvt. Ltd., "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Sales Management",
    "depends": [
        "crm",
        "product_operating_unit",
        "res_partner_operating_unit",
        "sale_operating_unit",
    ],
    "license": "AGPL-3",
    "data": [
        "security/ir.model.access.csv",
        "security/ir_rule.xml",
        "views/res_company.xml",
        "views/sale_order_view.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["max3903"],
}
