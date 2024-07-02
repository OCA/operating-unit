from odoo import api, fields, models


class POSPayment(models.Model):
    _inherit = "pos.payment"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "pos_payment_operating_unit_rel",
        string="Operating Units",
    )
    config_id = fields.Many2one(related="session_id.config_id", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            pos_order_id = self.env["pos.order"].sudo().browse(vals.get("pos_order_id"))
            if pos_order_id.config_id:
                vals["operating_unit_ids"] = [
                    (6, 0, pos_order_id.config_id.operating_unit_ids.ids)
                ]
        return super().create(vals_list)
