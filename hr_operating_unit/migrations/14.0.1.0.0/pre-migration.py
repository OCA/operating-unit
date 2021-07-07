# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from openupgradelib import openupgrade

_column_renames = {
    "operating_unit_employees_rel": [
        ("poid", "operating_unit_id"),
    ],
}


@openupgrade.migrate()
def migrate(env, version):
    if openupgrade.column_exists(env.cr, "operating_unit_employees_rel", "poid"):
        openupgrade.rename_columns(env.cr, _column_renames)
