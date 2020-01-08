# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.model
    def _default_warehouse_id(self):
        res = super(SaleOrder, self)._default_warehouse_id()
        team = self._get_default_team()
        warehouses = self.env['stock.warehouse'].search(
            [('operating_unit_id', '=', team.sudo().operating_unit_id.id)],
            limit=1)
        if warehouses:
            return warehouses
        return res

    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        default=_default_warehouse_id)

    @api.onchange('team_id')
    def onchange_team_id(self):
        super(SaleOrder, self).onchange_team_id()
        if self.team_id and self.team_id.operating_unit_id:
            warehouses = self.env['stock.warehouse'].search(
                [('operating_unit_id', '=',
                  self.team_id.operating_unit_id.id)],
                limit=1)
            if warehouses:
                self.warehouse_id = warehouses[0]

    @api.onchange('operating_unit_id')
    def onchange_operating_unit_id(self):
        if self.operating_unit_id:
            warehouses = self.env['stock.warehouse'].search(
                [('operating_unit_id', '=',
                  self.operating_unit_id.id)],
                limit=1)
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


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    @api.multi
    def _prepare_procurement_values(self, group_id=False):
        res = super(SaleOrderLine, self).\
            _prepare_procurement_values(group_id)
        res.update({
            'operating_unit_id':
                self.order_id.operating_unit_id.id,
        })
        return res

    @api.multi
    def _purchase_service_prepare_line_values(self, purchase_order,
                                              quantity=False):
        res = super(SaleOrderLine, self).\
            _purchase_service_prepare_line_values(
                purchase_order=purchase_order, quantity=quantity)
        res.update({
            'operating_unit_id':
                self.order_id.operating_unit_id.id,
        })
        return res
