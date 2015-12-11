# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class OperatingUnit(models.Model):

    _name = 'operating.unit'
    _description = 'Operating Unit'

    name = fields.Char('Name', size=256, required=True)
    code = fields.Char('Code', size=32, required=True)
    active = fields.Boolean('Active', default=True)
    company_id = fields.Many2one(
        'res.company', 'Company', required=True, default=lambda self:
        self.env['res.company']._company_default_get('account.account'))
    partner_id = fields.Many2one('res.partner', 'Partner', required=True)

    _sql_constraints = [
        ('code_company_uniq', 'unique (code,company_id)',
         'The code of the operating unit must '
         'be unique per company!'),
        ('name_company_uniq', 'unique (name,company_id)',
         'The name of the operating unit must '
         'be unique per company!')
    ]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            self = self.search([('code', operator, name)] + args, limit=limit)
            if not self:
                self = self.search([('name', operator, name)] + args,
                                   limit=limit)
        else:
            self = self.search(args, limit=limit)
        return self.name_get()
