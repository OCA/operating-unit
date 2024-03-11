# Copyright 2023 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class ResUsers(models.Model):
    _inherit = "res.users"

    def _get_default_warehouse_id(self):
        warehouse = self.env["stock.warehouse"].search(
            [
                ("company_id", "=", self.env.company.id),
                ("operating_unit_id", "=", self.env.user.default_operating_unit_id.id),
            ],
            limit=1,
        )
        if not warehouse:
            return super()._get_default_warehouse_id()
        return warehouse
