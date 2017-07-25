# -*- coding: utf-8 -*-
# Copyright 2015-17 Eficent Business and IT Consulting Services S.L.
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in MRP",
    "version": "10.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "license": "LGPL-3",
    "category": "Manufacturing",
    "depends": [
        "mrp",
        "procurement_operating_unit"
    ],
    "data": [
        "security/mrp_security.xml",
        "views/mrp_view.xml"
    ],
    'installable': True,
}
