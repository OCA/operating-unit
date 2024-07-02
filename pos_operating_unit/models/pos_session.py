from odoo import api, fields, models


class POSSession(models.Model):
    _inherit = "pos.session"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "pos_session_operating_unit_rel",
        string="Operating Units",
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            config_id = self.env["pos.config"].sudo().browse(vals.get("config_id"))
            if config_id:
                vals["operating_unit_ids"] = [(6, 0, config_id.operating_unit_ids.ids)]
        return super().create(vals_list)
