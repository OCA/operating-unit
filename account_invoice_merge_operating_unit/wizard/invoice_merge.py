# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, _
from odoo.exceptions import UserError


class InvoiceMerge(models.TransientModel):
    _inherit = "invoice.merge"

    @api.model
    def _dirty_check(self):
        res = super(InvoiceMerge, self)._dirty_check()
        if self.env.context.get('active_model', '') == 'account.invoice':
            ids = self.env.context['active_ids']
            invs = self.env['account.invoice'].browse(ids)
            for d in invs:
                if d['operating_unit_id'] != invs[0]['operating_unit_id']:
                    raise UserError(_('Not all invoices are at the same '
                                      'Operating Unit!'))
        return res
