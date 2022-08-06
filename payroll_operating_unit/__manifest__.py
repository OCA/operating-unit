# Copyright (C) 2022 Trevi Software (https://trevi.et)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Payroll Operating Unit",
    "summary": "Automatically set operating unit on payslip.",
    "version": "14.0.1.0.0",
    "category": "Payroll",
    "images": ["static/src/img/main_screenshot.png"],
    "author": "TREVI Software, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": [
        "hr_contract_operating_unit",
        "hr_operating_unit",
        "operating_unit",
        "payroll",
    ],
    "data": [
        "security/hr_payslip_security.xml",
        "views/hr_payslip_view.xml",
    ],
    "installable": True,
}
