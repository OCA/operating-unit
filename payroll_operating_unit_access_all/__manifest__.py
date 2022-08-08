# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Payroll Operating Unit Access",
    "summary": "Access all payslips.",
    "version": "14.0.1.0.0",
    "category": "Payroll",
    "images": ["static/src/img/main_screenshot.png"],
    "author": "TREVI Software, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": [
        "base",
        "payroll_operating_unit",
    ],
    "data": [
        "security/hr_payslip_security.xml",
    ],
    "installable": True,
}
