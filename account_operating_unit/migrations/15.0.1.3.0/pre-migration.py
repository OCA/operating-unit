# Copyright 2024 ForgeFlow S.L.  <https://www.forgeflow.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    if not openupgrade.column_exists(env.cr, "account_move_line", "is_ou_balance"):
        openupgrade.logged_query(
            env.cr,
            """
            ALTER TABLE account_move_line
            ADD COLUMN IF NOT EXISTS is_ou_balance BOOLEAN DEFAULT false
            """,
        )
        openupgrade.logged_query(
            env.cr,
            """ALTER TABLE account_move_line ALTER COLUMN is_ou_balance DROP DEFAULT""",
        )
        openupgrade.logged_query(
            env.cr,
            """
            UPDATE account_move_line aml0 SET is_ou_balance = true
            FROM account_move_line aml
            INNER JOIN res_company rc ON rc.id = aml.company_id
            WHERE aml.name = 'OU-Balancing'
            AND aml.account_id = rc.inter_ou_clearing_account_id
            AND rc.ou_is_self_balanced = true
            AND aml0.id = aml.id
        """,
        )
