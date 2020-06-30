# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

{
    "name": "Accounting Sequence by Operating Unit",
    "version": "13.0.1.0.0",
    "license": "AGPL-3",
    "category": "Accounting & Finance",
    "author": "Ecosoft, Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["account_operating_unit"],
    "data": ["views/operating_unit_view.xml"],
    "installable": True,
    "post_init_hook": "assign_ou_sequences",
}
