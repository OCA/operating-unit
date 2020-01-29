# Copyright 2019 Sunflower IT <https://www.sunflowerweb.nl>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl).

import logging
from odoo import models, api, fields
_logger = logging.getLogger(__name__)


class IrSequence(models.Model):
    _inherit = "ir.sequence"

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit',
        default=lambda self:
        self.env['res.users'].operating_unit_default_get(self._uid),
        domain="[('user_ids', '=', uid)]")

    @api.model
    def next_by_code(self, sequence_code):
        self.check_access_rights('read')
        force_company = self._context.get('force_company')
        if not force_company:
            force_company = self.env.user.company_id.id
        force_operating_unit = self._context.get('force_operating_unit')
        if not force_operating_unit:
            force_operating_unit = self.env.user.default_operating_unit_id.id
        seq_ids = self.search([
            ('code', '=', sequence_code),
            ('company_id', 'in', [force_company, False]),
            ('operating_unit_id', 'in', [force_operating_unit, False])
        ], order='company_id, operating_unit_id')
        if not seq_ids:
            _logger.debug(
                "No ir.sequence has been found for code '%s'. "
                "Please make sure a sequence is set for current company." %
                sequence_code
            )
            return False
        seq_id = seq_ids[0]
        return seq_id._next()
