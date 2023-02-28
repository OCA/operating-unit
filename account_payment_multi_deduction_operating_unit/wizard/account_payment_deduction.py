# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import api, fields, models


class AccountPaymentDeduction(models.TransientModel):
    _inherit = "account.payment.deduction"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        compute="_compute_operating_unit_multi_deduction",
        readonly=False,
        store=True,
        index=True,
    )

    @api.depends("payment_id")
    def _compute_operating_unit_multi_deduction(self):
        for rec in self:
            rec.operating_unit_id = rec.payment_id.deduct_operating_unit_id
