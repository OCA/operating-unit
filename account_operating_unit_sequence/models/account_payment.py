# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import _, api, models
from odoo.exceptions import UserError

MAP_SEQUENCE = {
    "customer": {
        "inbound": "payment_cust_inv_seq_id",
        "outbound": "payment_cust_refund_seq_id",
    },
    "supplier": {
        "inbound": "payment_supp_refund_seq_id",
        "outbound": "payment_supp_inv_seq_id",
    },
}


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def create(self, vals):
        if vals.get("name", "/") == "/" and vals.get("operating_unit_id", False):
            ou_id = self.env["operating.unit"].browse(vals["operating_unit_id"])
            if vals["payment_type"] == "transfer":
                sequence_id = ou_id.payment_transfer_seq_id
            else:
                if vals["partner_type"] and vals["payment_type"]:
                    sequence_id = ou_id[
                        MAP_SEQUENCE[vals["partner_type"]][vals["payment_type"]]
                    ]
            if sequence_id:
                vals["name"] = sequence_id.next_by_id()
        return super().create(vals)

    def post(self):
        if len(self.mapped("operating_unit_id")) != 1:
            raise UserError(
                _(
                    "The payment cannot be processed because "
                    "the operating units are different!"
                )
            )
        for rec in self:
            ou_id = rec.operating_unit_id
            if ou_id:
                # keep the name in case of a payment reset to draft
                if not rec.name:
                    # Use the right sequence to set the name
                    if rec.payment_type == "transfer":
                        sequence_id = ou_id.payment_transfer_seq_id
                    else:
                        if rec.partner_type and rec.payment_type:
                            sequence_id = ou_id[
                                MAP_SEQUENCE[rec.partner_type][rec.payment_type]
                            ]
                    if sequence_id:
                        rec.name = sequence_id.next_by_id()
        return super().post()
