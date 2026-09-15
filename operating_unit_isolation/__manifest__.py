# Copyright 2016-2026 CIT Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Operating Unit Isolation",
    "summary": "An extension to provide isolation for operating units",
    "version": "18.0.1.0.0",
    "author": "CIT Services, Odoo Community Association (OCA)",
    "company": "CIT Services",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Generic",
    "depends": ["base", "operating_unit"],
    "data": [],
    "assets": {
        "web.assets_backend": [
            "operating_unit_isolation/static/src/js/operating_unit_isolation.esm.js"
        ],
    },
    "license": "AGPL-3",
    "installable": True,
}
