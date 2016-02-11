# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Operating Unit in CRM",
    "version": "8.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "http://www.eficent.com",
    "category": "Purchase Management",
    "depends": ["crm", "operating_unit"],
    "description": """
Operating Unit in CRM
=====================
This module introduces the operating unit to CRM
    """,
    "data": [
        "views/crm_lead_view.xml",
        "security/crm_security.xml",
    ],
    'installable': True,
    'active': False,
}
