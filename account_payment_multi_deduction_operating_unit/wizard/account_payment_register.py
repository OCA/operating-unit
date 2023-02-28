# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = "account.payment.register"

    deduct_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute="_compute_default_operating_unit",
    )
    writeoff_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        index=True,
    )

    def _update_vals_deduction(self, moves):
        res = super()._update_vals_deduction(moves)
        operating_units = moves.mapped("operating_unit_id")
        self.writeoff_operating_unit_id = (
            len(operating_units) == 1 and operating_units.id or False
        )
        return res

    def _create_payment_vals_from_wizard(self):
        payment_vals = super()._create_payment_vals_from_wizard()
        if (
            not self.currency_id.is_zero(self.payment_difference)
            and self.payment_difference_handling == "reconcile"
        ):
            payment_vals["write_off_line_vals"][
                "operating_unit_id"
            ] = self.writeoff_operating_unit_id.id
        return payment_vals

    @api.depends("payment_difference", "deduction_ids")
    def _compute_default_operating_unit(self):
        active_ids = self.env.context.get("active_ids")
        moves = self.env["account.move"].browse(active_ids)
        operating_units = moves.mapped("operating_unit_id")
        for rec in self:
            rec.deduct_operating_unit_id = (
                len(operating_units) == 1 and operating_units.id or False
            )

    def _prepare_deduct_move_line(self, deduct):
        vals = super()._prepare_deduct_move_line(deduct)
        vals.update(
            {
                "operating_unit_id": deduct.operating_unit_id
                and deduct.operating_unit_id.id
                or False,
            }
        )
        return vals
