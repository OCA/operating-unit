# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "HR Timesheet Operating Unit",
    "version": "20.0.1.0.0",
    "author": "Jarsa, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Human Resources",
    "depends": ["hr_timesheet", "account_operating_unit"],
    "data": [
        "views/account_analytic_line_views.xml",
    ],
    "installable": True,
    "auto_install": True,
}
