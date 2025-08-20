# Copyright 2025 Simone Rubino - PyTech
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).

from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.convert_to_company_dependent(
        env,
        "res.users",
        openupgrade.get_legacy_name("default_operating_unit_id"),
        "default_operating_unit_id",
    )
