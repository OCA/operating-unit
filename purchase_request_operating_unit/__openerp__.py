# -*- coding: utf-8 -*-
# © 2016 Eficent
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in Purchase Requests",
    "version": "9.0.1.0.0",
    "author": "Eficent"
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "http://www.eficent.com",
    "category": "Purchase Management",
    "depends": ["purchase_request",
                "purchase_operating_unit"],
    "data": [
        "view/purchase_request_view.xml",
        "security/purchase_security.xml",
    ],
    'installable': True,
}
