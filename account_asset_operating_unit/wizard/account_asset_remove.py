# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountAssetRemove(models.TransientModel):
    _inherit = "account.asset.remove"

    def remove(self):
        res = super().remove()
        asset_id = self.env.context.get("active_id")
        asset = self.env["account.asset"].browse(asset_id)
        move = False
        if isinstance(res, dict):
            if "domain" in res.keys() and "res_model" in res.keys():
                if res["res_model"] == "account.move":
                    move = self.env["account.move"].search(res["domain"])
        # Assign operating unit to journal entry if any
        if asset and move:
            move.operating_unit_id = asset.operating_unit_id
            move._onchange_invoice_line_ids()
        return res
