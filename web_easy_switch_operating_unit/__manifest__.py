# Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
# Copyright (C) Startx 2021
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Easy Switch Operating Unit",
    "version": "18.0.1.0.0",
    "category": "web",
    "author": "Startx, ICTSTUDIO, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["web", "operating_unit"],
    "data": ["views/res_users_views.xml"],
    'assets': {
        'web.assets_backend': [
            'web_easy_switch_operating_unit/static/src/js/*',
            'web_easy_switch_operating_unit/static/src/xml/switch_operating_unit.xml',
        ],
    }
}
