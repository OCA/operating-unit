##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

from odoo import api, fields, models


class ResUsers(models.Model):

    _inherit = 'res.users'

    operating_unit_for_mails_id = fields.Many2one(
        'operating.unit', 'Operating Unit For Mails',
        domain="[('id', 'in', operating_unit_ids)]"
    )

    @api.onchange('operating_unit_ids')
    def _on_change_operating_unit_ids(self):
        if (self.operating_unit_for_mails_id and
                self.operating_unit_for_mails_id.id not in self.operating_unit_ids.ids):
            self.operating_unit_for_mails_id = False
