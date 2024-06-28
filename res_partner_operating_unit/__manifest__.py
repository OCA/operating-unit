# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2020 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Partner with Operating Unit",
    "summary": "Introduces Operating Unit fields in Partner",
    "version": "17.0.1.0.0",
    "author": "Edi Santoso, "
    "Niaga Solution, "
    "Serpent Consulting Services Pvt. Ltd., "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Generic",
    "depends": ["operating_unit"],
    "license": "LGPL-3",
    "data": ["security/res_partner_security.xml", "views/res_partner_view.xml"],
    "installable": True,
    "pre_init_hook": "pre_init_hook",
}
