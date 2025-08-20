# Copyright 2025 Simone Rubino - PyTech
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    # Save the value that will be restored as company-dependent
    openupgrade.rename_columns(
        env.cr,
        {
            "res_users": [
                ("default_operating_unit_id", None),
            ],
        },
    )
