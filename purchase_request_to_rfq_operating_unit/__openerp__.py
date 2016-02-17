# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Purchase Request to RFQ with Operating Units",
    "version": "9.0.1.0.0",
    "author": "Eficent"
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "http://www.eficent.com",
    "category": "Purchase Management",
    "depends": ["purchase_request_to_rfq", "purchase_request_operating_unit"],
    "data": [
        "wizard/purchase_request_line_make_purchase_order_view.xml",
    ],
    'installable': True,
}
