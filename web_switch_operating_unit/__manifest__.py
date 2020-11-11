# © 2020 Vishnu Vanneri
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Easy Operating Unit Switching",

    "summary": """
        User With Multiple Operating Unit (OU) Can Easily Switch From Menu""",
    "version": "12.0.1.0.0",
    "author": "Vanneri,"
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Hidden",
    "depends": ["web", "operating_unit"],
    "license": "LGPL-3",
    "data": [
        "views/web_switch_operating_unit.xml",
    ],
    "qweb": [
        "static/src/xml/switch_op.xml",
    ],
}
