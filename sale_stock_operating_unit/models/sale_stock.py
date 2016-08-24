# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, models, _
from openerp.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = 'stock.move'

    @api.model
    def _prepare_picking_assign(self, move):
        """
        Override to add Operating Units to Picking.
        """
        values = super(StockMove, self)._prepare_picking_assign(move)
        sale_line = move.procurement_id and move.procurement_id.sale_line_id
        if sale_line:
            values.update({
                'operating_unit_id': sale_line.order_id and
                sale_line.order_id.operating_unit_id.id
            })
        return values


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
            if self.team_id and self.team_id.operating_unit_id != \
                    self.operating_unit_id:
                self.team_id = False

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
