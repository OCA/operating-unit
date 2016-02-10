# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Operating Unit in Sales Stock",
    "version": "7.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Purchase Management",
    "depends": ["sale_stock",
                "sale_operating_unit",
                "stock_operating_unit"],
    "description": """
Operating Unit in Sales Stock
=============================
This module prevents a user from selecting a Warehouse in the Sale Shop
that does not belong to the same operating unit.


Credits
=======

Contributors
------------

* Jordi Ballester <jordi.ballester@eficent.com>

    """,
    "data": [],
    'installable': True,
    'active': False,
}
