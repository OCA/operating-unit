# Copyright 2016-19 Eficent Business and IT Consulting Services S.L.
# Copyright 2016-19 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).).

from odoo import fields, models


class StockLandedCost(models.Model):

    _inherit = "stock.landed.cost"

    operating_unit_id = fields.Many2one(
        "operating.unit",
        "Operating Unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self._uid
        ),
    )

    def button_validate(self):
        res = super().button_validate()
        if self.account_move_id:
            move = self.env["account.move"]
            move = self.account_move_id
            move.line_ids.operating_unit_id = self.operating_unit_id.id
        return res
