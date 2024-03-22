{
    "name": "Operating Unit Custom Header",
    "summary": """Custom header and footer by operating unit on reports""",
    "author": "ArcheTI, " "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "report",
    "version": "14.0.1.0.0",
    "license": "LGPL-3",
    "depends": [
        "base",
        "operating_unit",
    ],
    "data": [
        "views/templates.xml",
        "views/operating_unit_views.xml",
    ],
    "post_init_hook": "post_init_hook",
}
