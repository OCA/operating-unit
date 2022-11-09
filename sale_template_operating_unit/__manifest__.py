# Copyright (C) 2021 Pavlov Media
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Operating Unit in Sale Templates",
    "version": "14.0.1.0.0",
    "summary": "An operating unit (OU) is an organizational entity part of a "
    "company",
    "author": "Pavlov Media, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Sales Management",
    "depends": [
        "operating_unit",
        "sale_management",
    ],
    "data": [
        "security/sale_template_security.xml",
        "views/sale_template_view.xml",
    ],
    "installable": True,
}
