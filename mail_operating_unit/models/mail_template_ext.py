##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import fields, models


class MailTemplateExt(models.Model):
    _inherit = 'mail.template'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit')
