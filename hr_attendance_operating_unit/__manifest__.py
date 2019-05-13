# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "HR Attendance Operating Unit",
    "version": "12.0.1.0.0",
    "author": "Gonzalo González Domínguez, "
              "Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Human Resources",
    "depends": ["hr", "operating_unit", "hr_operating_unit"],
    "data": [
        "security/security.xml",
        "views/hr_attendance.xml",
    ],
    'installable': True,
}