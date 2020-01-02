# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    def get_default_lead_description_template(self):
        return
        """
${object.partner_shipping_id._display_address()}
%for line in object.line_ids
${line.name}: ${line.qty} ${line.uom_id.name}
%endfor
        """

    lead_description_template = fields.Text(
        string='Lead Description Template',
        default=get_default_lead_description_template(),
        help="Template used to provide the information for an operating unit "
             "to quote another.")
