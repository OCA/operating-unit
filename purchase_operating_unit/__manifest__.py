# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# Copyright 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in Purchase Orders",
    "summary": "An operating unit (OU) is an organizational entity part of a "
               "company",
    "version": "11.0.1.1.1",
    "author": "Eficent, "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "https://www.github.com/oca/operating-unit",
    "category": "Purchase Management",
    "depends": ["stock_operating_unit", "purchase"],
    "license": "LGPL-3",
    "data": [
        "security/purchase_security.xml",
        "views/purchase_order_view.xml",
        "views/purchase_order_line_view.xml",
    ],
    "demo": [
        "demo/purchase_order_demo.xml",
    ],
    "installable": True,
}
