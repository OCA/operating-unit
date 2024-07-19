# Copyright (C) 2020 Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def pre_init_hook(env):
    # Add new table and columns to hold values
    env.cr.execute(
        """
        CREATE TABLE operating_unit_partner_rel (
            partner_id INTEGER NOT NULL
                REFERENCES res_partner(id) ON DELETE CASCADE,
            operating_unit_id INTEGER NOT NULL
                REFERENCES operating_unit(id) ON DELETE CASCADE);
    """
    )
    # Add the values
    env.cr.execute(
        """
        INSERT INTO operating_unit_partner_rel
            (partner_id, operating_unit_id)
        SELECT id, 1 FROM res_partner;
    """
    )
