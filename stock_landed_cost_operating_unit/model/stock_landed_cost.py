from odoo import _, api, fields, models
from odoo.exceptions import UserError

from odoo.addons.stock_landed_costs.models.stock_landed_cost \
    import LandedCost as LandedCost

import logging
_logger = logging.getLogger(__name__)


class StockLandedCost(models.Model):
    _inherit = 'stock.landed.cost'

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit')

    @api.model
    def _default_operating_unit(self):
        return self.env.user.operating_unit_default_id

    @api.model
    def _default_show_operating_unit(self):
        return len(self.env.user.operating_unit_ids) > 1

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        default=_default_operating_unit
    )

    show_operating_unit = fields.Boolean(
        compute="_compute_show_operating_unit",
        default="_default_show_operating_unit")

    @api.multi
    def _compute_show_operating_unit(self):
        for item in self:
            item.show_operating_unit = \
                len(self.env.user.operating_unit_ids) > 1

    @api.model_cr
    def _register_hook(self):
        """ MonkeyPatch method only when module is installed on the DB.
        The patched method is a copy of standard name_get adding name2.
        The original function pointer to name_get is stored in 'origin'
        attribute.
        The patch need to be removed when module is uninstalled. This is
        done in the uninstall hook during runtime. No server restart
        needed.

        """
        res = super(StockLandedCost, self)._register_hook()

        @api.multi
        def button_validate(self):
            if any(cost.state != 'draft' for cost in self):
                raise UserError(_('Only draft landed costs can be validated'))
            if any(not cost.valuation_adjustment_lines for cost in self):
                raise UserError(_('No valuation adjustments lines. You should '
                                  'maybe recompute the landed costs.'))
            if not self._check_sum():
                raise UserError(
                    _('Cost and adjustments lines do not match. You should '
                      'maybe recompute the landed costs.'))

            for cost in self:
                move = self.env['account.move']
                ##########################################################
                # hack by mara1 - Adding operating unit
                move_vals = {
                    'journal_id': cost.account_journal_id.id,
                    'date': cost.date,
                    'ref': cost.name,
                    'line_ids': [],
                    'operating_unit_id': cost.operating_unit_id.id,
                }
                ###########################################################
                for line in cost.valuation_adjustment_lines.filtered(
                        lambda line: line.move_id):
                    # Prorate the value at what's still in stock
                    cost_to_add = ((line.move_id.remaining_qty /
                                   line.move_id.product_qty) *
                                   line.additional_landed_cost)

                    new_landed_cost_value = line.move_id.landed_cost_value + \
                        line.additional_landed_cost
                    ##########################################################
                    # hack by mara1 - Adding operating unit
                    line.move_id.write({
                        'landed_cost_value': new_landed_cost_value,
                        'value': (line.move_id.value +
                                  line.additional_landed_cost),
                        'remaining_value': (line.move_id.remaining_value +
                                            cost_to_add),
                        'price_unit': ((line.move_id.value +
                                       line.additional_landed_cost) /
                                       line.move_id.product_qty),
                        'operating_unit_id': cost.operating_unit_id.id,
                    })
                    ###########################################################
                    # `remaining_qty` is negative if the move is out and
                    # delivered proudcts that were not in stock.
                    qty_out = 0
                    if line.move_id._is_in():
                        qty_out = (line.move_id.product_qty -
                                   line.move_id.remaining_qty)
                    elif line.move_id._is_out():
                        qty_out = line.move_id.product_qty
                    move_vals['line_ids'] += line._create_accounting_entries(
                        move, qty_out)

                move = move.create(move_vals)
                cost.write({'state': 'done', 'account_move_id': move.id})
                move.post()
            return True

        origin = getattr(LandedCost.button_validate, 'origin', None)
        if origin != button_validate:
            LandedCost._patch_method('button_validate', button_validate)
            _logger.info('LandedCost.button_validate method'
                         ' patched to add operating unit!')

        return res
