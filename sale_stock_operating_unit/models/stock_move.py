# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _get_new_picking_values(self):
        """
        Override to add Operating Units to Picking.
        """
        values = super(StockMove, self)._prepare_picking_assign()
        sale_line = self.procurement_id and self.procurement_id.sale_line_id
        if sale_line:
            values.update({
                'operating_unit_id': sale_line.order_id and
                sale_line.order_id.operating_unit_id.id
            })
        return values
