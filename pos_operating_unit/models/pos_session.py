# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class PosSession(models.Model):
    _inherit = "pos.session"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        readonly=True,
    )

    @api.model
    def create(self, values):
        config_id = values.get("config_id") or self.env.context.get("default_config_id")
        pos_config = self.env["pos.config"].browse(config_id)
        if pos_config.operating_unit_id:
            values["operating_unit_id"] = pos_config.operating_unit_id.id
        return super().create(values)

    def _get_sale_vals(self, key, amount, amount_converted):
        res = super()._get_sale_vals(key, amount, amount_converted)
        move = self.env["account.move"].browse(res["move_id"])
        move.write({"operating_unit_id": self.operating_unit_id.id})
        res["operating_unit_id"] = self.operating_unit_id.id
        return res

    def _credit_amounts(
        self,
        partial_move_line_vals,
        amount,
        amount_converted,
        force_company_currency=False,
    ):
        res = super()._credit_amounts(
            partial_move_line_vals, amount, amount_converted, force_company_currency
        )
        res["operating_unit_id"] = self.operating_unit_id.id
        return res

    def _debit_amounts(
        self,
        partial_move_line_vals,
        amount,
        amount_converted,
        force_company_currency=False,
    ):
        res = super()._debit_amounts(
            partial_move_line_vals, amount, amount_converted, force_company_currency
        )
        res["operating_unit_id"] = self.operating_unit_id.id
        return res
