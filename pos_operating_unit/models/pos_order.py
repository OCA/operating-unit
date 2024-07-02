from odoo import api, fields, models


class POSOrder(models.Model):
    _inherit = "pos.order"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "pos_order_operating_unit_rel",
        string="Operating Units",
    )
    config_id = fields.Many2one(related="session_id.config_id", readonly=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            session_id = self.env["pos.session"].sudo().browse(vals.get("session_id"))
            if session_id.config_id:
                vals["operating_unit_ids"] = [
                    (6, 0, session_id.config_id.operating_unit_ids.ids)
                ]
        return super().create(vals_list)


class POSOrderLine(models.Model):
    _inherit = "pos.order.line"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "pos_order_line_operating_unit_rel",
        string="Operating Units",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            order_id = self.env["pos.order"].sudo().browse(vals.get("order_id"))
            if order_id.config_id:
                vals["operating_unit_ids"] = [
                    (6, 0, order_id.config_id.operating_unit_ids.ids)
                ]
        return super().create(vals_list)
