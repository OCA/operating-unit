# Copyright (C) 2020 Pavlov Media
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

{
    "name": "Mail Template Operating Unit",
    "version": "14.0.1.0.0",
    "author": "Pavlov Media, " "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Base",
    "depends": [
        "operating_unit",
        "mail",
    ],
    "data": [
        "views/mail_template_view.xml",
        "security/mail_security.xml",
    ],
    "installable": True,
    "maintainers": ["patrickrwilson"],
}
