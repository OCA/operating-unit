# -*- coding: utf-8 -*-
# © 2015 Eficent - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.tools.translate import _
from openerp import api, fields, models
from openerp.exceptions import UserError


class StockWarehouse(models.Model):
    _inherit = "stock.warehouse"

    operating_unit_id = fields.Many2one('operating.unit',
                                        'Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))


class StockLocation(models.Model):
    _inherit = 'stock.location'

    operating_unit_id = fields.Many2one('operating.unit',
                                        'Operating Unit')

    @api.one
    @api.constrains('operating_unit_id')
    def _check_warehouse_operating_unit(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse = warehouse_obj.search([('wh_input_stock_loc_id', 'in',
                                           self.ids)])
        for w in warehouse:
            if self.operating_unit_id != w.operating_unit_id:
                raise UserError(_('Configuration error!\nThis location is\
                                assigned to a warehouse that belongs to a\
                                different operating unit.'))
        warehouse = warehouse_obj.search([('lot_stock_id', 'in', self.ids)])
        for w in warehouse:
            if self.operating_unit_id != w.operating_unit_id:
                raise UserError(_('Configuration error!\nThis location is\
                                assigned to a warehouse that belongs to a\
                                different operating unit.'))
        warehouse = warehouse_obj.search([('wh_output_stock_loc_id', 'in',
                                           self.ids)])
        for w in warehouse:
            if self.operating_unit_id != w.operating_unit_id:
                raise UserError(_('Configuration error!\nThis location is\
                assigned to a warehouse that belongs to a different\
                operating unit.'))

    def _check_required_operating_unit(self, cr, uid, ids, context=None):
        return True
        for l in self.browse(cr, uid, ids, context=context):
            if l.usage == 'internal' and not l.operating_unit_id:
                return False
            if l.usage != 'internal' and l.operating_unit_id:
                return False
        return True

    @api.one
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        if self.company_id and self.operating_unit_id and\
                self.company_id != self.operating_unit_id.company_id:
            raise UserError(_('Configuration error!\nThe Company in the\
            Stock Location and in the Operating Unit must be the same.'))

    @api.one
    @api.constrains('operating_unit_id', 'location_id')
    def _check_parent_operating_unit(self):
        if (self.location_id and self.location_id.usage == 'internal'
            and self.operating_unit_id and self.operating_unit_id !=
                self.location_id.operating_unit_id):
                raise UserError(_('Configuration error!\nThe Parent\
                Stock Location must belong to the same Operating Unit.'))

    _constraints = [
        (_check_required_operating_unit,
         'The operating unit should be assigned to internal locations, '
         'and to non other.', ['operating_unit_id'])]


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    operating_unit_id = fields.Many2one('operating.unit',
                                        'Requesting Operating Unit',
                                        default=lambda self:
                                        self.env['res.users'].
                                        operating_unit_default_get(self._uid))

    @api.one
    @api.constrains('operating_unit_id', 'company_id')
    def _check_company_operating_unit(self):
        if self.company_id and self.operating_unit_id and \
                self.company_id != self.operating_unit_id.company_id:
            raise UserError(_('Configuration error!\nThe Company in the\
            Stock Picking and in the Operating Unit must be the same.'))

    @api.one
    @api.constrains('operating_unit_id', 'move_lines')
    def _check_stock_move_operating_unit(self):
        if not self.operating_unit_id:
            return True
        operating_unit = self.operating_unit_id
        for sm in self.move_lines:
            if (
                sm.location_id and
                sm.location_id.operating_unit_id and
                operating_unit != sm.location_id.operating_unit_id
            ) and (
                sm.location_dest_id and
                sm.location_dest_id.operating_unit_id and
                operating_unit !=
                    sm.location_dest_id.operating_unit_id
            ):
                raise UserError(_('Configuration error!\nThe Stock moves\
                must be related to a location (source or destination)\
                that belongs to the requesting Operating Unit.'))

    _constraints = [
        (_check_stock_move_operating_unit,
         'The Stock moves must be related to a location (source or '
         'destination) that belongs to the requesting Operating Unit.',
         ['operating_unit_id', 'move_lines'])
    ]


class StockMove(models.Model):
    _inherit = 'stock.move'

    operating_unit_id =\
        fields.Many2one('operating.unit',
                        related='location_id.operating_unit_id',
                        string='Source Location Operating Unit', readonly=True)
    operating_unit_dest_id =\
        fields.Many2one('operating.unit',
                        related='location_dest_id.operating_unit_id',
                        string='Dest. Location Operating Unit', readonly=True)
