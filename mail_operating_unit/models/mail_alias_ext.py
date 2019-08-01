##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import fields, models, api


class MailAliasExt(models.Model):
    _inherit = 'mail.alias'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit')

    @api.multi
    def _get_alias_domain(self):
        super(MailAliasExt, self)._get_alias_domain()
        for record in self:
            if record.operating_unit_id:
                record.alias_domain = record.operating_unit_id.catchall_domain
