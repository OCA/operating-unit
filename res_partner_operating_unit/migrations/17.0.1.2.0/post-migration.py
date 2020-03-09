# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openupgradelib import openupgrade

_deleted_xml_records = [
    "res_partner_operating_unit.ir_rule_res_partner_allowed_operating_units",
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.delete_records_safely_by_xml_id(
        env,
        _deleted_xml_records,
    )
