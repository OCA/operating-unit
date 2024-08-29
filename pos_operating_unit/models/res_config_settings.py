from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    pos_operating_unit_ids = fields.Many2many(
        related="pos_config_id.operating_unit_ids",
        readonly=False,
    )
