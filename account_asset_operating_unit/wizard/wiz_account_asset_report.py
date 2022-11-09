# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from odoo import api, fields, models


class WizAccountAssetReport(models.TransientModel):
    _inherit = "wiz.account.asset.report"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=lambda self: self._default_operating_unit_id(),
    )

    @api.model
    def _default_operating_unit_id(self):
        return []
