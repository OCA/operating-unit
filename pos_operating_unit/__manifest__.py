# © 2019 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
{
    "name": "Operating Unit in Point Of Sales",
    "version": "12.0.1.0.1",
    "summary": "An operating unit (OU) is an organizational entity part of a "
               "company",
    "author": "Mind And Go, "
              "Eficent, "
              "Serpent Consulting Services Pvt. Ltd.,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Sales Management",
    "depends": ["point_of_sale", 
                "pos_sale",
                "account_operating_unit", 
                "sales_team_operating_unit",
                
                ],
    "data": [
        "security/pos_security.xml",
        "views/pos_view.xml",
#         "views/sale_report_view.xml",
    ],
    'installable': True
}
