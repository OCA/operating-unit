##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import api, fields, models


class MailComposeMessageExt(models.TransientModel):
    _inherit = 'mail.compose.message'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit')

    @api.model
    def default_get(self, fields):
        result = super(MailComposeMessageExt, self).default_get(fields)
        model = result.get('model', False)
        res_id = result.get('res_id', False)
        if model and res_id:
            model_object = self.env[model].browse(res_id)
            if hasattr(model_object, 'operating_unit_id'):
                result['operating_unit_id'] = model_object.operating_unit_id.id
        return result
