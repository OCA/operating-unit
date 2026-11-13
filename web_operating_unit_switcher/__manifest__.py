# Copyright (C) 2026 CIT-Services <https://cit-services.eu/>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Operating Unit Switcher",
    "version": "18.0.1.0.0",
    "category": "web",
    "author": "CIT-Services, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["web", "operating_unit"],
    "data": ["views/res_users_views.xml"],
    "assets": {
        "web.assets_backend": [
            "web_operating_unit_switcher/static/src/js/*",
            "web_operating_unit_switcher/static/src/xml/switch_operating_unit.xml",
        ],
        "web.assets_unit_tests": [
            "web_operating_unit_switcher/static/tests/*.test.js",
        ],
    },
}
