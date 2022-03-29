# Copyright 2021 Jarsa
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).


def migrate(cr, installed_version):
    cr.execute(
        "ALTER TABLE stock_quant ADD COLUMN IF NOT EXISTS operating_unit_id int4;"
    )
    cr.execute(
        """
        UPDATE stock_quant
        SET operating_unit_id = sl.operating_unit_id
        FROM stock_location sl
        WHERE sl.id=location_id AND sl.operating_unit_id IS NOT NULL;
    """
    )
