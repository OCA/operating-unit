# Copyright (C) 2020 Pavlov Media
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).e.

from odoo import fields, models


class HrEmployee(models.Model):
    _inherit = "hr.employee"

    default_operating_unit_id = fields.Many2one(
        'operating.unit',
        related='user_id.default_operating_unit_id'
    )
    operating_unit_ids = fields.Many2many(
        'operating.unit',
        related='user_id.operating_unit_ids'
    )
