# Copyright 2016-19 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2016-19 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in Purchase Requests",
    "version": "14.0.1.0.0",
    "author": "Eficent, SerpentCS, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "license": "LGPL-3",
    "category": "Purchase Management",
    "depends": ["purchase_request", "purchase_operating_unit"],
    "data": [
        "security/purchase_security.xml",
        "view/purchase_request_view.xml",
        "wizard/purchase_request_line_make_purchase_order_view.xml",
    ],
    "installable": True,
}
