# Copyright 2025 Camptocamp SA
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _get_orders_with_single_partner_ou_without_team(self):
        return self.filtered(
            lambda so: not so.team_id and len(so.partner_id.operating_unit_ids) == 1
        )

    @api.depends("partner_id.operating_unit_ids")
    def _compute_team_id(self):
        # For orders without a team and whose partner has exactly one operating unit,
        # skip the team computation by excluding those orders from the computation.
        orders_to_skip = self._get_orders_with_single_partner_ou_without_team()
        if orders_to_skip:
            self = self - orders_to_skip
        return super()._compute_team_id()

    @api.depends("team_id", "partner_id.operating_unit_ids")
    def _compute_operating_unit_id(self):
        # OVERRIDE: orders where no team is set and whose partners
        # have exactly 1 OU should use the partner's OU itself
        if ou_from_partner := self._get_orders_with_single_partner_ou_without_team():
            self -= ou_from_partner
            for order in ou_from_partner:
                order.operating_unit_id = order.partner_id.operating_unit_ids
        return super()._compute_operating_unit_id()
