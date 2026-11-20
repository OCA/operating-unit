# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

{
    "name": "Operating Units for Timesheets",
    "summary": "Manage timesheets per operating unit",
    "version": "18.0.1.0.0",
    "category": "Services/Timesheets",
    "website": "https://github.com/OCA/operating-unit",
    "author": "Coop IT Easy SC, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "hr_timesheet",
        "project_operating_unit",
    ],
    "data": [
        "security/account_analytic_line_security.xml",
    ],
}
