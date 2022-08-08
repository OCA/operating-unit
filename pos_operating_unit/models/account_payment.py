# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.model
    def create(self, values):
        if values.get("pos_session_id"):
            session = self.env["pos.session"].browse(values["pos_session_id"])
            values["operating_unit_id"] = session.operating_unit_id.id
        return super().create(values)
