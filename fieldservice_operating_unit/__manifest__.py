# Copyright (C) 2021 Open Source Integrators
# Copyright (C) 2021 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Field Service with Operating Units",
    "summary": """
        This module adds operating unit information to Field Service orders.""",
    "version": "14.0.1.0.0",
    "author": "Open Source Integrators, "
    "Serpent Consulting Services Pvt. Ltd.,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Field Service",
    "depends": ["operating_unit", "fieldservice"],
    "license": "AGPL-3",
    "data": [
        "security/fieldservice_security.xml",
        "views/fsm_order.xml",
    ],
    "installable": True,
    "development_status": "Beta",
    "maintainers": [
        "max3903",
    ],
}
