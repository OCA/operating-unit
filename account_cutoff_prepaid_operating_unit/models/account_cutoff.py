# -*- coding: utf-8 -*-
# © 2013-2016 Akretion (Alexis de Lattre <alexis.delattre@akretion.com>)
# © 2018 Magnus (Willem Hulshof <w.hulshof@magnus.nl>)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class AccountCutoff(models.Model):
    _inherit = 'account.cutoff'

    def _prepare_prepaid_lines(self, aml, mapping):
        res = super(AccountCutoff, self)._prepare_prepaid_lines(aml, mapping)
        res['operating_unit_id'] = aml.operating_unit_id.id
        return res



