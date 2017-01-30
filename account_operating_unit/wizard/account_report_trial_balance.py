# -*- coding: utf-8 -*-
# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class AccountBalanceReport(models.TransientModel):
    _inherit = "account.balance.report"

    operating_unit_ids = fields.Many2many(
        'operating.unit', 'account_balance_report_operating_unit_rel',
        'account_id', 'operating_unit_id', string='Operating Units',
        required=False,
        default=[])

    def _build_contexts(self, data):
        result = super(AccountBalanceReport, self)._build_contexts(data)
        data2 = {}
        data2['form'] = self.read(['operating_unit_ids'])[0]
        result['operating_unit_ids'] = 'operating_unit_ids' \
                                       in data2['form'] and \
                                       data2['form']['operating_unit_ids'] \
                                       or False
        return result

    def _print_report(self, data):
        operating_units = ', '.join([ou.name for ou in
                                     self.operating_unit_ids])
        data['form'].update({'operating_units': operating_units})
        return super(AccountBalanceReport, self)._print_report(data)
