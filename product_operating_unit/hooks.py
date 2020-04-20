# Copyright (C) 2020 Open Source Integrators
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def pre_init_hook(cr):
    # Add new table and columns to hold values
    cr.execute("""
        CREATE TABLE product_operating_unit_rel (
            product_template_id INTEGER NOT NULL
                REFERENCES product_template(id) ON DELETE CASCADE,
            operating_unit_id INTEGER NOT NULL
                REFERENCES operating_unit(id) ON DELETE CASCADE);
    """)
    # Add the values
    cr.execute("""
        INSERT INTO product_operating_unit_rel
            (product_template_id, operating_unit_id)
        SELECT id, 1 FROM product_template;
    """)
