# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, models


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
