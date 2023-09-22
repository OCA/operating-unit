# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Work Acceptance Operating Unit",
    "summary": "Introduces Operating Unit (OU) in work acceptance",
    "version": "14.0.1.0.0",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Purchase Management",
    "depends": ["purchase_work_acceptance", "purchase_operating_unit"],
    "license": "AGPL-3",
    "data": [
        "security/purchase_work_acceptance_security.xml",
        "views/work_acceptance_views.xml",
    ],
    "installable": True,
}
