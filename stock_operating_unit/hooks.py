# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import SUPERUSER_ID
from odoo.api import Environment


def update_operating_unit_location(cr, registry):
    env = Environment(cr, SUPERUSER_ID, {})
    warehouses = env["stock.warehouse"].search([])
    for warehouse in warehouses:
        operating_unit = warehouse.operating_unit_id
        parent_location = warehouse.view_location_id
        locations = env["stock.location"].search(
            [("id", "child_of", [parent_location.id]), ("usage", "=", "internal")]
        )
        if operating_unit:
            query = """update stock_location set operating_unit_id = %s where
            location_id in %s or id in %s"""
            cr.execute(
                query, (operating_unit.id, tuple(locations.ids), tuple(locations.ids))
            )
    return True
