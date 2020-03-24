# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import api, fields, models


class ResCompany(models.Model):
    _inherit = 'res.company'

    @api.model
    def _get_default_lead_description_template(self):
        return """Notes:
${object.notes}

Delivery Address:
${object.sale_id.partner_shipping_id.name}
${object.sale_id.partner_shipping_id.street}
${object.sale_id.partner_shipping_id.street2}
${object.sale_id.partner_shipping_id.city}, \
${object.sale_id.partner_shipping_id.state_id.name}, \
${object.sale_id.partner_shipping_id.zip}
${object.sale_id.partner_shipping_id.country_id.name}

Products:
%for line in object.line_ids
- ${line.name}: ${line.qty} ${line.uom_id.name}
%endfor"""

    lead_description_template = fields.Text(
        string='Lead Description Template',
        required=True,
        default=_get_default_lead_description_template,
        help="Template used to provide the information for an operating unit "
             "to quote another.")
