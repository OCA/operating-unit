# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class OperatingUnit(models.Model):

    _name = 'operating.unit'
    _description = 'Operating Unit'

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    active = fields.Boolean(default=True)
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
        # Make a search with default criteria
        names1 = super(models.Model, self).name_search(
            name=name, args=args, operator=operator, limit=limit)
        # Make the other search
        names2 = []
        if name:
            domain = [('code', '=ilike', name + '%')]
            names2 = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names1) | set(names2))[:limit]
