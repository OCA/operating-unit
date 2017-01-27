# -*- coding: utf-8 -*-
# © 2015-17 Eficent
# - Jordi Ballester Alomar
# © 2015-17 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import Warning


class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        default=lambda self: self.env['res.users'].
        operating_unit_default_get(self._uid),
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if rec.company_id and rec.operating_unit_id and \
                    rec.company_id != rec.operating_unit_id.company_id:
                raise Warning(_('The Company in the Move Line and in the '
                                'Operating Unit must be the same.'))


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        related='crossovered_budget_id.operating_unit_id',
        string='Operating Unit', readonly=True, store=True,
    )
