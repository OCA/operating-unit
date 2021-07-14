# Copyright (C) 2021 Open Source Integrators
# Copyright (C) 2021 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).lgpl.html).

from odoo import api, models


class CRMLead(models.Model):

    _inherit = "crm.lead"

    @api.onchange("date_deadline")
    def _onchange_date_deadline(self):
        if self.date_deadline:
            quote_ids = self.env["sale.order.quote"].search(
                [("lead_id", "=", self.name)]
            )
            quote_ids.write({"expected_date": self.date_deadline})
