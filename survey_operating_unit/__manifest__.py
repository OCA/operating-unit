# Copyright 2025 Giuseppe Borruso - Dinamiche Aziendali srl
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    "name": "Survey with Operating Units",
    "summary": "Adds the concept of operating unit (OU) in surveys",
    "version": "16.0.1.0.0",
    "category": "Generic Modules/Surveys",
    "author": "Giuseppe Borruso - Dinamiche Aziendali srl, Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["survey", "operating_unit"],
    "data": [
        "security/survey_security.xml",
        "views/survey_survey_view.xml",
        "views/survey_user_input_view.xml",
    ],
    "installable": True,
}
