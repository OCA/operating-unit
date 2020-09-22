# Copyright 2020 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models


class ResUsers(models.Model):

    _inherit = "res.users"

    def _accessible_operating_units(self):
        """Add all children to OUs from field"""
        manual = super()._accessible_operating_units()
        return self.env["operating.unit"].search([("id", "child_of", manual.ids)])
