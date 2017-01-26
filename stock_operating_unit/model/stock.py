# -*- coding: utf-8 -*-
# © 2016-2017 Eficent Business and IT Consulting Services S.L.
# © 2016-2017 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import _, api, fields, models
from openerp.exceptions import UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    def _default_operating_unit(self):
        if self.company_id:
            company = self.company_id
        else:
            company = self.env['res.company']._company_default_get(
                'stock.inventory')
        for ou in self.env.user.operating_unit_ids:
            if company == self.company_id:
                self.operating_unit_id = ou

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=_default_operating_unit
    )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise UserError(
                    _('Configuration error\nThe Company in the Stock Warehouse'
                      ' and in the Operating Unit must be the same.')
                )


class StockLocation(models.Model):
    _inherit = 'stock.location'

    operating_unit_id = fields.Many2one('operating.unit',
                                        'Operating Unit')

    @api.multi
    @api.constrains('operating_unit_id')
    def _check_warehouse_operating_unit(self):
        for rec in self:
            warehouse_obj = self.env['stock.warehouse']
            warehouses = warehouse_obj.search(
                ['|', '|', ('wh_input_stock_loc_id', '=', rec.ids[0]),
                 ('lot_stock_id', 'in', rec.ids),
                 ('wh_output_stock_loc_id', 'in', rec.ids)])
            for w in warehouses:
                if rec.operating_unit_id != w.operating_unit_id:
                    raise UserError(_('Configuration error\nThis location is '
                                      'assigned to a warehouse that belongs to'
                                      ' a different operating unit.'))
                if self.operating_unit_id != w.operating_unit_id:
                    raise UserError(_('Configuration error\nThis location is '
                                      'assigned to a warehouse that belongs to'
                                      ' a different operating unit.'))
                if rec.operating_unit_id != w.operating_unit_id:
                    raise UserError(_('Configuration error\nThis location is'
                                      ' assigned to a warehouse that belongs'
                                      ' to a different operating unit.'))

    @api.multi
    @api.constrains('operating_unit_id')
    def _check_required_operating_unit(self):
        for rec in self:
            if rec.usage == 'internal' and not rec.operating_unit_id:
                raise UserError(
                    _('Configuration error\nThe operating unit should be '
                      'assigned to internal locations and to non other.')
                )
            if rec.usage != 'internal' and rec.operating_unit_id:
                raise UserError(
                    _('Configuration error\nThe operating unit should be '
                      'assigned to internal locations and to non other.')
                )

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise UserError(
                    _('Configuration error\nThe Company in the Stock Location '
                      'and in the Operating Unit must be the same.'))

    @api.multi
    @api.constrains('operating_unit_id', 'location_id')
    def _check_parent_operating_unit(self):
        for rec in self:
            if (
                rec.location_id and
                rec.location_id.usage == 'internal' and
                rec.operating_unit_id and
                rec.operating_unit_id != rec.location_id.operating_unit_id
            ):
                raise UserError(
                    _('Configuration error\nThe Parent Stock Location '
                      'must belong to the same Operating Unit.')
                )


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    operating_unit_id = fields.Many2one('operating.unit',
                                        'Requesting Operating Unit',
                                        readonly=1)

    @api.onchange('picking_type_id', 'partner_id')
    def onchange_picking_type(self):
        res = super(StockPicking, self).onchange_picking_type()
        if self.picking_type_id:
            picking_type = self.env['stock.picking.type'].browse(
                self.picking_type_id.id) or None
            if picking_type:
                unit = picking_type.warehouse_id.operating_unit_id
                if unit:
                    res['value']['operating_unit_id'] = unit.id
        return res

    @api.multi
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        for rec in self:
            if (rec.company_id and rec.operating_unit_id and
                    rec.company_id != rec.operating_unit_id.company_id):
                raise UserError(
                    _('Configuration error\nThe Company in the Stock Picking '
                      'and in the Operating Unit must be the same.')
                )

    @api.multi
    @api.constrains('operating_unit_id', 'picking_type_id')
    def _check_picking_type_operating_unit(self):
        for rec in self:
            warehouse = rec.picking_type_id.warehouse_id
            if (rec.picking_type_id and rec.operating_unit_id and
                    warehouse.operating_unit_id != rec.operating_unit_id):
                raise UserError(
                    _('Configuration error\nThe Operating Unit of the picking '
                      'must be the same as that of the warehouse of the '
                      'Picking Type.')
                )


class StockMove(models.Model):
    _inherit = 'stock.move'

    operating_unit_id = fields.Many2one(
        related='location_id.operating_unit_id',
        string='Source Location Operating Unit',
        readonly=True,
    )
    operating_unit_dest_id = fields.Many2one(
        related='location_dest_id.operating_unit_id',
        string='Dest. Location Operating Unit',
        readonly=True,
    )

    @api.multi
    @api.constrains('operating_unit_id', 'location_id', 'picking_id',
                    'operating_unit_dest_id', 'location_dest_id')
    def _check_stock_move_operating_unit(self):
        for stock_move in self:
            if not stock_move.operating_unit_id:
                return True
            operating_unit = stock_move.operating_unit_id
            operating_unit_dest = stock_move.operating_unit_dest_id
            if (stock_move.location_id and
                stock_move.location_id.operating_unit_id and
                stock_move.picking_id and
                operating_unit != stock_move.picking_id.operating_unit_id
                ) and (
                stock_move.location_dest_id and
                stock_move.location_dest_id.operating_unit_id and
                stock_move.picking_id and
                operating_unit_dest != stock_move.picking_id.operating_unit_id
            ):
                raise UserError(
                    _('Configuration error\nThe Stock moves must '
                      'be related to a location (source or destination) '
                      'that belongs to the requesting Operating Unit.')
                )
