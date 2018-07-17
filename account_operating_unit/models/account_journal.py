# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class AccountJournal(models.Model):
    _inherit = "account.journal"

    operating_unit_id = fields.Many2one(comodel_name='operating.unit',
                                        string='Operating Unit',
                                        help="Operating Unit that will be "
                                             "used in payments, when this "
                                             "journal is used.")

    @api.multi
    @api.constrains('type')
    def _check_ou(self):
        for journal in self:
            if journal.type in ('bank', 'cash') \
                    and journal.company_id.ou_is_self_balanced \
                    and not journal.operating_unit_id:
                raise UserError(_('Configuration error!\nThe operating unit '
                                  'must be indicated in bank journals, '
                                  'if it has been defined as self-balanced '
                                  'at company level.'))
