# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in MRP",
    "version": "9.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "license": "LGPL-3",
    "category": "Manufacturing",
    "depends": ["mrp",
                "procurement_operating_unit"],
    "description": """
Operating Unit in MRP
=======================================
This module implements global security rules on manufacturing orders so that
a user can only read manufacturing orders where the location is linked to an
operating unit that the user has access to.

Credits
=======

Contributors
------------

* Jordi Ballester <jordi.ballester@eficent.com>

    """,
    "data": [
        "security/mrp_security.xml",
        "views/mrp_view.xml"
    ],
    'installable': True,
}
