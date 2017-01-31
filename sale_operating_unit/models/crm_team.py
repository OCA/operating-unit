# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, models
from odoo.exceptions import ValidationError


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    @api.multi
    @api.constrains('operating_unit_id')
    def _check_sales_order_operating_unit(self):
        for rec in self:
            orders = self.env['sale.order'].search(
                [('team_id', '=', rec.id), ('operating_unit_id', '!=',
                                            rec.operating_unit_id.id)])
            if orders:
                raise ValidationError(_('Sales orders already exist '
                                        'referencing this team in other '
                                        'operating units.'))
