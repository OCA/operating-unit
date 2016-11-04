# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp import api, models, _
from openerp.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('team_id')
    def onchange_team_id(self):
        self.operating_unit_id = self.team_id.operating_unit_id

    @api.multi
    @api.constrains('team_id', 'operating_unit_id')
    def _check_team_operating_unit(self):
        for rec in self:
            if rec.team_id and rec.team_id.operating_unit_id != \
                    rec.operating_unit_id:
                raise ValidationError(_('Configuration error!\n'
                                        'The Operating Unit of the sales team '
                                        'must match with that of the '
                                        'quote/sales order'))
