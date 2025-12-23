# Copyright (C) 2020 Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def migrate(env, version):
    if not version:
        return

    # Add the values
    env.execute(
        """
        INSERT INTO operating_unit_partner_rel(
            partner_id, operating_unit_id
        )
        SELECT rp.id, 1 FROM res_partner AS rp left JOIN operating_unit_partner_rel
        AS op ON op.partner_id = rp.id WHERE op.partner_id is  null;
    """
    )
