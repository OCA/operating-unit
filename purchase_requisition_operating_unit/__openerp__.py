# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in Purchase Requisitions",
    "version": "9.0.1.0.0",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "Purchase Management",
    "depends": ["purchase_requisition",
                "purchase_operating_unit"],
    "description": """
Operating Unit in Purchase Requisitions
=======================================
This module was written to extend the Purchase Requsition capabilities of Odoo.

This module introduces the operating unit to the purchase requisition.

Security rules are defined to ensure that users can only display the
Purchase Requisitions in which they are allowed access to.

Installation
============

No additional installation instructions are required.


Configuration
=============

This module does not require any additional configuration.

Usage
=====

At the time when a user creates a new purchase requisition the system
proposes the user's default operating unit.

The operating unit is a required field.

When the user creates a purchase order (PO) from the purchase requisition the
operating unit is copied to the PO.


Known issues / Roadmap
======================

No issue has been identified.

Credits
=======

Contributors
------------

* Jordi Ballester <jordi.ballester@eficent.com>

Maintainer
----------

.. image:: http://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.


    """,
    "data": [
        "view/purchase_requisition.xml",
        "security/purchase_security.xml",
    ],
    'installable': True,
}
