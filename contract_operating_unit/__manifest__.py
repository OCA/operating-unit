# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Contract Operating Unit",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ForgeFlow S.L., Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Invoicing",
    "depends": ["contract", "account_operating_unit"],
    "data": ["views/contract_view.xml", "security/contract_security.xml"],
    "installable": True,
}
