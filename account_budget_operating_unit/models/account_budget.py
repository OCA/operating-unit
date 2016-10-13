# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, fields, models, _
from openerp.exceptions import Warning


class CrossoveredBudget(models.Model):
    _inherit = "crossovered.budget"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        string='Operating Unit',
        default=lambda self: self.env['res.users'].
        operating_unit_default_get(self._uid),
    )

    @api.one
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        if self.company_id and self.operating_unit_id and \
                self.company_id != self.operating_unit_id.company_id:
            raise Warning(_('The Company in the Move Line and in the '
                            'Operating Unit must be the same.'))


class CrossoveredBudgetLines(models.Model):
    _inherit = "crossovered.budget.lines"

    operating_unit_id = fields.Many2one(
        'operating.unit',
        related='crossovered_budget_id.operating_unit_id',
        string='Operating Unit', readonly=True, store=True,
    )
