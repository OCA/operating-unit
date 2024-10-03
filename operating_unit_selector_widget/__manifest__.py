# Copyright 2024-TODAY Jérémy Didderen
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Operating Unit - Selector Widget",
    "summary": "Widget dedicated to choose the active operating units.",
    "version": "17.0.1.0.0",
    "author": "Jérémy Didderen, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Generic",
    "depends": [
        "operating_unit",
    ],
    "license": "LGPL-3",
    "assets": {
        "web.assets_backend": [
            "operating_unit_selector_widget/static/src/operating_unit_service.esm.js",
            "operating_unit_selector_widget/static/src/switch_operating_unit_menu/switch_operating_unit_menu.xml",
            "operating_unit_selector_widget/static/src/switch_operating_unit_menu/switch_operating_unit_menu.esm.js",
        ],
        "web.qunit_suite_tests": ["operating_unit_selector_widget/static/tests/*.js"],
    },
}
