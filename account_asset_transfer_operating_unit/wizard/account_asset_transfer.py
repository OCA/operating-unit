# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountAssetTransfer(models.TransientModel):
    _inherit = "account.asset.transfer"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
    )

    @api.model
    def default_get(self, field_list):
        res = super().default_get(field_list)
        from_asset_ids = self.env.context.get("active_ids")
        assets = self.env["account.asset"].browse(from_asset_ids)
        # Prepare default values
        operating_unit_id = assets.mapped("operating_unit_id")
        res["operating_unit_id"] = (
            operating_unit_id.id if len(operating_unit_id) == 1 else False
        )
        return res

    def _get_new_move_transfer(self):
        move_values = super()._get_new_move_transfer()
        move_values["operating_unit_id"] = self.operating_unit_id.id
        return move_values

    def _get_move_line_from_asset(self, move_line):
        move_lines = super()._get_move_line_from_asset(move_line)
        move_lines["operating_unit_id"] = move_line.operating_unit_id.id
        return move_lines

    def _get_move_line_to_asset(self, to_asset):
        move_lines = super()._get_move_line_to_asset(to_asset)
        move_lines["operating_unit_id"] = (to_asset.operating_unit_id.id,)
        return move_lines


class AccountAssetTransferLine(models.TransientModel):
    _inherit = "account.asset.transfer.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute="_compute_asset_transfer_operating_unit",
        readonly=False,
        store=True,
        string="Operating Unit",
    )

    @api.depends("transfer_id.operating_unit_id")
    def _compute_asset_transfer_operating_unit(self):
        for rec in self:
            rec.operating_unit_id = rec.transfer_id.operating_unit_id
