# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class AccountAsset(models.Model):
    _inherit = "account.asset"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        default=lambda self: self.env["res.users"].operating_unit_default_get(
            self.env.user.id
        ),
    )

    @api.model
    def _xls_acquisition_fields(self):
        res = super()._xls_acquisition_fields()
        return res + ["operating_unit"]

    @api.model
    def _xls_active_fields(self):
        res = super()._xls_active_fields()
        return res + ["operating_unit"]

    @api.model
    def _xls_removal_fields(self):
        res = super()._xls_removal_fields()
        return res + ["operating_unit"]
