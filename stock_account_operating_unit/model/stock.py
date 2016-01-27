# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models
from openerp.tools.translate import _
from openerp.exceptions import UserError


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.model
    def _prepare_account_move_line(self, move, qty, cost, credit_account_id,
                                       debit_account_id):
        res = super(StockQuant, self).\
            _prepare_account_move_line(move, qty, cost, credit_account_id,
                                       debit_account_id)

        debit_line_vals = res[0][2]
        credit_line_vals = res[1][2]

        if (
            move.operating_unit_id and move.operating_unit_dest_id and
            move.operating_unit_id != move.operating_unit_dest_id and
            debit_line_vals['account_id'] != credit_line_vals['account_id']
        ):
            raise UserError(_('You cannot create stock moves involving '
                                   'separate source and destination accounts '
                                   'and different source and destination '
                                   'operating units.'))

        debit_line_vals['operating_unit_id'] = \
            move.operating_unit_dest_id.id or move.operating_unit_id.id
        credit_line_vals['operating_unit_id'] = \
            move.operating_unit_id.id or move.operating_unit_dest_id.id
        return [(0, 0, debit_line_vals), (0, 0, credit_line_vals)]

    @api.multi
    def _create_product_valuation_moves(self, move):
        """
        Generate an accounting moves if the product being moved is subject
        to real_time valuation tracking,
        and the source or destination location are
        a transit location or is outside of the company or the source or
        destination locations belong to different operating units.
        """
        res = super(StockQuant, self)._create_product_valuation_moves(move)

        if move.product_id.valuation == 'real_time':
            # Inter-operating unit moves do not accept to
            # from/to non-internal location
            if (
                move.location_id.company_id ==
                    move.location_dest_id.company_id and
                    move.operating_unit_id != move.operating_unit_dest_id
            ):
                err = False
                if move.location_id.usage != 'internal' \
                        and move.location_dest_id.usage == 'internal':
                    err = True
                if move.location_id.usage != 'internal' \
                        and move.location_dest_id.usage == 'internal':
                    err = True
                if move.location_id.usage != 'internal' \
                        and move.location_dest_id.usage != 'internal':
                    err = True
                if err:
                    raise UserError(_('Transfers between locations of '
                          'different operating unit locations is only allowed '
                          'when both source  and destination locations are '
                          'internal.'))
                src_company_ctx = dict(
                    context, force_company=move.location_id.company_id.id)
                company_ctx = dict(context, company_id=move.company_id.id)
                journal_id, acc_src, acc_dest, acc_valuation = \
                    self._get_accounting_data_for_valuation(move,
                                                            src_company_ctx)
                reference_amount, reference_currency_id = \
                    self._get_reference_accounting_values_for_valuation(
                        move, src_company_ctx)
                account_moves = []
                account_moves += [(journal_id, self._create_account_move_line(
                    move, acc_valuation, acc_valuation,
                    reference_amount, reference_currency_id))]
                move_obj = self.pool.get('account.move')
                for j_id, move_lines in account_moves:
                    move_obj.create({'journal_id': j_id,
                                     'line_id': move_lines,
                                     'company_id': move.company_id.id,
                                     'ref': move.picking_id and
                                     move.picking_id.name},
                                    context=company_ctx)
