# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def create(self, vals):
        if vals.get("operating_unit_id", False):
            seq_date = None
            if "date_order" in vals:
                seq_date = fields.Datetime.context_timestamp(
                    self, fields.Datetime.to_datetime(vals["date_order"])
                )
            sequence_code = (
                self.env["operating.unit"]
                .browse(vals["operating_unit_id"])
                .purchase_sequence_id.code
            )
            if sequence_code:
                vals["name"] = self.env["ir.sequence"].next_by_code(
                    sequence_code, sequence_date=seq_date
                )
        return super().create(vals)
