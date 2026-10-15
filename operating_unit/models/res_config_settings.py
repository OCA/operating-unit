# Copyright 2026 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    new_user_operating_unit_ids = fields.Many2many(
        related="company_id.new_user_operating_unit_ids",
        readonly=False,
    )
    new_user_default_operating_unit_id = fields.Many2one(
        related="company_id.new_user_default_operating_unit_id",
        readonly=False,
    )
