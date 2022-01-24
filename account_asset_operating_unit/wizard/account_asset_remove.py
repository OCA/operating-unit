# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountAssetRemove(models.TransientModel):
    _inherit = "account.asset.remove"

    def remove(self):
        res = super().remove()
        asset_id = self.env.context.get("active_id")
        asset = self.env["account.asset"].browse(asset_id)
        move = self.env["account.move"].search(res["domain"])
        if asset and move:
            move.operating_unit_id = asset.operating_unit_id
            move._onchange_invoice_line_ids()
        return res
