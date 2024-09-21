# Copyright 2024 ForgeFlow S.L.  <https://www.forgeflow.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move_line aml0 SET display_type = 'ou_balance'
        FROM account_move_line aml
        INNER JOIN res_company rc ON rc.id = aml.company_id
        WHERE aml.name = 'OU-Balancing'
        AND aml.account_id = rc.inter_ou_clearing_account_id
        AND rc.ou_is_self_balanced = true
        AND aml0.id = aml.id
    """,
    )
