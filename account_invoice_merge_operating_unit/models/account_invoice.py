# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.model
    def _get_invoice_line_key_cols(self):
        res = super(AccountInvoice, self)._get_invoice_line_key_cols()
        res.append('operating_unit_id')
        return res

    @api.model
    def _get_first_invoice_fields(self, invoice):
        res = super(AccountInvoice, self)._get_first_invoice_fields(invoice)
        res.update({'operating_unit_id': invoice.operating_unit_id.id})
        return res
