# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class FakeThread(models.Model):
    """Minimal mail.thread model with an operating unit, for tests only."""

    _name = "mail.operating.unit.fake.thread"
    _inherit = ["mail.thread"]
    _description = "Fake Thread (mail_operating_unit tests)"

    name = fields.Char()
    operating_unit_id = fields.Many2one("operating.unit", string="Operating Unit")
