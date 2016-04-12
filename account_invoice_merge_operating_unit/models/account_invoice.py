# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.osv import orm


class AccountInvoice(orm.Model):
    _inherit = 'account.invoice'

    def _get_invoice_line_key_cols(self, cr, uid, invoice_line):
        res = super(AccountInvoice, self)._get_invoice_line_key_cols(
            cr, uid, invoice_line)
        res = list(res)
        res.append('operating_unit_id')
        return tuple(res)

    def _get_first_invoice_fields(self, cr, uid, invoice):
        res = super(AccountInvoice, self)._get_first_invoice_fields(cr, uid,
                                                                    invoice)
        res.update({'operating_unit_id': invoice.operating_unit_id.id})
        return res
