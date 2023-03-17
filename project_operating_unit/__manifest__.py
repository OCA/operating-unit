# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Project with Operating Units",
    "summary": """
        This module adds operating unit information to projects and tasks.""",
    "version": "16.0.1.0.0",
    "author": "Open Source Integrators, "
    "Serpent Consulting Services Pvt. Ltd., "
    "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Project",
    "depends": [
        "operating_unit",
        "project",
    ],
    "license": "AGPL-3",
    "data": [
        "security/project_security.xml",
        "views/project_project.xml",
        "views/project_task.xml",
    ],
    "development_status": "Beta",
    "maintainers": ["max3903"],
}
