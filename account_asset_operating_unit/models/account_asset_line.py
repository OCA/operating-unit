# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountAssetLine(models.Model):
    _inherit = "account.asset.line"

    def _setup_move_data(self, depreciation_date):
        move_data = super()._setup_move_data(depreciation_date)
        if self.asset_id.operating_unit_id:
            move_data.update({"operating_unit_id": self.asset_id.operating_unit_id.id})
        return move_data

    def create_move(self):
        created_move_ids = super().create_move()
        moves = self.env["account.move"].browse(created_move_ids)
        for move in moves:
            move._onchange_invoice_line_ids()
        return created_move_ids
