# Copyright (C) 2021 Open Source Integrators
# Copyright (C) 2021 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Agreement with Operating Units",
    "summary": """
        This module adds operating unit information to agreements and service
        profiles.""",
    "version": "14.0.1.0.0",
    "author": "Open Source Integrators, "
    "Serpent Consulting Services Pvt. Ltd.,"
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Agreement",
    "depends": ["operating_unit", "agreement_serviceprofile"],
    "license": "AGPL-3",
    "data": [
        "security/aggreement_security.xml",
        "views/agreement.xml",
        "views/agreement_serviceprofile.xml",
    ],
    "installable": True,
    "development_status": "Beta",
    "maintainers": [
        "max3903",
    ],
}
