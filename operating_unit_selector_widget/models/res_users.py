# Copyright 2024-TODAY Jérémy Didderen
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import logging

from odoo import _, models
from odoo.exceptions import AccessError

_logger = logging.getLogger(__name__)


class ResUsers(models.Model):
    _inherit = "res.users"

    def operating_units(self):
        operating_unit_ids = self.env.context.get("allowed_ou_ids", [])
        user_ou_ids = self.operating_unit_ids.ids
        if operating_unit_ids:
            if not self.env.su:
                if set(operating_unit_ids) - set(user_ou_ids):
                    raise AccessError(_("Access to unauthorized or invalid companies."))
            return self.env["operating.unit"].browse(operating_unit_ids)
        return self.env["operating.unit"].browse(user_ou_ids)
