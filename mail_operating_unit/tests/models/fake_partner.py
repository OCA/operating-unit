# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class FakePartner(models.Model):
    _name = "res.partner"
    _inherit = "res.partner"
    _description = "Fake Partner"

    operating_unit_id = fields.Many2one("operating.unit", string="Operating Unit")
