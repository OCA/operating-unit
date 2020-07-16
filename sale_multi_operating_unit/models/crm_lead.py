# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, models


class CRMLead(models.Model):

    _inherit = 'crm.lead'

    @api.onchange('date_deadline')
    def onchange_date_deadline(self):
        if self.date_deadline:
            quote_ids = self.env['sale.order.quote'].\
                search([('lead_id', '=', self.name)])
            if quote_ids:
                for quote_id in quote_ids:
                    quote_id.write({'expected_date': self.date_deadline})
