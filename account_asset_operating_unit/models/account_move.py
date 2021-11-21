# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountMove(models.Model):
    _inherit = "account.move"

    def _prepare_asset_vals(self, aml):
        res = super()._prepare_asset_vals(aml)
        res.update({"operating_unit_id": aml.operating_unit_id})
        return res
