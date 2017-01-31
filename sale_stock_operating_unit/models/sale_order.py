# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('team_id')
    def onchange_team_id(self):
        super(SaleOrder, self).onchange_team_id()
        if self.team_id and self.team_id.operating_unit_id:
            warehouses = self.env['stock.warehouse'].search(
                [('operating_unit_id', '=',
                  self.team_id.operating_unit_id.id)])
            if warehouses:
                self.warehouse_id = warehouses[0]

    @api.onchange('operating_unit_id')
    def onchange_operating_unit_id(self):
        if self.operating_unit_id:
            warehouses = self.env['stock.warehouse'].search(
                [('operating_unit_id', '=',
                  self.operating_unit_id.id)])
            if warehouses:
                self.warehouse_id = warehouses[0]

    @api.onchange('warehouse_id')
    def onchange_warehouse_id(self):
        if self.warehouse_id:
            self.operating_unit_id = self.warehouse_id.operating_unit_id
            if self.team_id and self.team_id.operating_unit_id != \
                    self.operating_unit_id:
                self.team_id = False

    @api.multi
    @api.constrains('operating_unit_id', 'warehouse_id')
    def _check_wh_operating_unit(self):
        for rec in self:
            if rec.operating_unit_id and rec.operating_unit_id != \
                    rec.warehouse_id.operating_unit_id:
                raise ValidationError(_('Configuration error!\nThe Operating'
                                        'Unit in the Sales Order and in the'
                                        ' Warehouse must be the same.'))
