# Copyright 2015-19 ForgeFlow S.L. -
# Jordi Ballester Alomar
# © 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# © 2026 CIT Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "MIS Builder with Operating Unit",
    "version": "18.0.0.1.0",
    "category": "Reporting",
    "author": "ForgeFlow, "
    "Serpent Consulting Services Pvt. Ltd.,"
    "ACSONE SA/NV,"
    "CIT Services,"
    "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["mis_builder", "account_operating_unit"],
    "data": ["security/mis_builder_security.xml", "view/mis_builder.xml"],
    "installable": True,
}
