# © 2019 Eficent Business and IT Consulting Services S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class StockMove(models.Model):
    _inherit = 'stock.move'

    operating_unit_id = fields.Many2one(
        related='location_id.operating_unit_id',
        string='Source Location Operating Unit',
    )
    operating_unit_dest_id = fields.Many2one(
        related='location_dest_id.operating_unit_id',
        string='Dest. Location Operating Unit',
    )

    @api.multi
    @api.constrains('picking_id', 'location_id', 'location_dest_id')
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
                    _('Configuration error. The Stock moves must '
                      'be related to a location (source or destination) '
                      'that belongs to the requesting Operating Unit.')
                )
