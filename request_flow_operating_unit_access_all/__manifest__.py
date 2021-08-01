# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "Access all OUs' request_flow",
    "version": "14.0.1.0.0",
    "author": "Ecosoft,Odoo Community Association (OCA)",
    "category": "Sales",
    "license": "AGPL-3",
    "website": "https://github.com/OCA/operating-unit",
    "depends": ["request_flow_operating_unit"],
    "data": [
        "security/request_security.xml",
    ],
    "installable": True,
    "maintainers": ["kittiu"],
}
