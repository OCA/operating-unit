# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    def _account_entry_move(self, move):
        """
        Generate accounting moves if the product being moved is subject
        to real_time valuation tracking,
        and the source or destination location are
        a transit location or is outside of the company or the source or
        destination locations belong to different operating units.
        """
        res = super(StockQuant, self)._account_entry_move(move)
        if move.product_id.valuation == 'real_time':
            # Inter-operating unit moves do not accept to
            # from/to non-internal location
            if (
                move.location_id.company_id ==
                    move.location_dest_id.company_id and
                    move.operating_unit_id != move.operating_unit_dest_id
            ):
                src_company_ctx = dict(
                    force_company=move.location_id.company_id.id
                )
                company_ctx = dict(company_id=move.company_id.id)
                self = self.with_context(src_company_ctx)
                (journal_id, acc_src, acc_dest, acc_valuation) = \
                    move._get_accounting_data_for_valuation()
                quant_cost_qty = {}
                for quant in self:
                    if quant_cost_qty.get(quant.cost):
                        quant_cost_qty[quant.cost] += quant.qty
                    else:
                        quant_cost_qty[quant.cost] = quant.qty
                move_obj = self.env['account.move']
                for cost, qty in quant_cost_qty.items():
                    move_lines = move._prepare_account_move_line(qty, cost,
                                                                 acc_valuation,
                                                                 acc_valuation)
                    move_obj.with_context(company_ctx).create({
                        'journal_id': journal_id,
                        'line_ids': move_lines,
                        'company_id': move.company_id.id,
                        'ref': move.picking_id and move.picking_id.name,
                    })
        return res
