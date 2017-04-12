# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# © 2015 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Operating Unit in CRM Claims",
    "version": "9.0.1.0.0",
    "author": "Eficent, "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "http://www.eficent.com",
    "category": "Sales",
    "depends": ["crm_claim", "operating_unit", "sales_team_operating_unit"],
    "data": [
        "security/crm_security.xml",
        "views/crm_claim_view.xml"
    ],
    'installable': True,
}
