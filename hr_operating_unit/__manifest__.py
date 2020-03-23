# Copyright (C) 2020 Pavlov Media
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Employees - Operating Units',
    'summary': """
        Show related users operating units on employees""",
    'version': "12.0.1.1.0",
    'author': "Pavlov Media",
              "Odoo Community Association (OCA)"
    'website': "https://github.com/OCA/operating-unit",
    'category': "HR",
    'depends': [
        'operating_unit',
        'hr'
    ],
    'license': "AGPL-3",
    'data': [
        'views/hr_employee.xml',
    ],
    'development_status': 'Beta',
    'maintainers': ['patrickrwilson'],
}
