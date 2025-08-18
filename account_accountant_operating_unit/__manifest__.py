##############################################################################
# Copyright (c) 2025 braintec AG (https://braintec.com)
# All Rights Reserved
#
# Licensed under the LGPL-3.0 (http://www.gnu.org/licenses/lgpl.html)
##############################################################################

{
    "name": "Account Accountant Operating Unit (BRIDGE)",
    "version": "17.0.1.0.0",
    "summary": """
        Adds Operating Unit to be used in reconciliation for companies where
        'Operating Units are self-balanced' is set""",
    "category": "Accounting/Accounting",
    "author": "braintec AG",
    "website": "https://github.com/OCA/operating-unit",
    "license": "LGPL-3",
    "depends": ["account_accountant", "account_operating_unit"],
    "installable": True,
    "auto_install": True,
}
