# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.depends("journal_id")
    def _compute_operating_unit_id(self):
        for payment in self:
            if payment.journal_id:
                payment.operating_unit_id = payment.journal_id.operating_unit_id

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        domain="[('user_ids', '=', uid)]",
        compute="_compute_operating_unit_id",
        store=True,
    )

    def _prepare_payment_moves(self):
        res = super()._prepare_payment_moves()
        if not self.operating_unit_id:
            return res
        for move in res:
            bank_journal = self.env["account.journal"].browse(move["journal_id"])
            bank_ou_id = bank_journal.operating_unit_id.id
            for line in move["line_ids"]:
                line[2]["operating_unit_id"] = bank_ou_id
        bank_account_id = self.journal_id.default_debit_account_id.id
        if self.payment_type == "outbound":
            bank_account_id = self.journal_id.default_credit_account_id.id
        if self.invoice_ids and len(self.invoice_ids) == 1:
            invoice_ou_id = self.invoice_ids.operating_unit_id.id
            for move in res:
                for line in move["line_ids"]:
                    if line[2]["account_id"] != bank_account_id:
                        line[2]["operating_unit_id"] = invoice_ou_id
        return res
