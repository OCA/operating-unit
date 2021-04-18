# -*- coding: utf-8 -*-
# © 2013-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 Magnus (Willem Hulshof <w.hulshof@magnus.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountCutoff(models.Model):
    _inherit = 'account.cutoff'

    def _prepare_accrual_date_lines(self, aml, mapping):
        res = super(AccountCutoff, self)._prepare_accrual_date_lines(aml, mapping)
        res['operating_unit_id'] = aml.operating_unit_id.id

        # if aml.tax_ids:
        #     # It won't work with price-included taxes
        #     for tax in aml.tax_ids:
        #         if tax.price_include:
        #             raise UserError(_(
        #                 "Price included taxes such as '%s' are not "
        #                 "supported by the module account_cutoff_accrual_dates "
        #                 "for the moment.") % tax.display_name)
        #     tax_compute_all_res = aml.tax_ids.compute_all(
        #         cutoff_amount, product=aml.product_id, partner=aml.partner_id)
        #     res['tax_line_ids'] = self._prepare_tax_lines(
        #         tax_compute_all_res, self.company_currency_id)
        return res

