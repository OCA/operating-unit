from odoo import fields, models


class POSConfig(models.Model):
    _inherit = "pos.config"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        "pos_config_operating_unit_rel",
        string="Operating Units",
    )
