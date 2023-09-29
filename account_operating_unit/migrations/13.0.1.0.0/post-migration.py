from openupgradelib import openupgrade


def fill_account_move_operating_unit(env):
    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move_line aml
        SET operating_unit_id = ail.operating_unit_id
        FROM account_invoice_line ail
        WHERE aml.old_invoice_line_id = ail.id
        AND aml.operating_unit_id is NULL""",
    )

    openupgrade.logged_query(
        env.cr,
        """
        UPDATE account_move am
        SET operating_unit_id = ai.operating_unit_id
        FROM account_invoice ai
        WHERE am.old_invoice_id = ai.id
        AND am.operating_unit_id is NULL""",
    )


@openupgrade.migrate()
def migrate(env, version):
    fill_account_move_operating_unit(env)
