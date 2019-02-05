# Copyright 2015-19 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models
from odoo.exceptions import ValidationError
from odoo.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('opportunity_id', 'operating_unit_id')
    def _check_sale_operating_unit(self):
        if self.opportunity_id and self.opportunity_id.operating_unit_id and\
                self.opportunity_id.\
                operating_unit_id != self.operating_unit_id:
            raise ValidationError(_('''The Operating Unit of Sales Order does
                not match to that of the Opportunity.'''))

    @api.constrains('opportunity_id', 'user_id')
    def _check_saleperson(self):
        if self.opportunity_id and self.opportunity_id.user_id and \
                self.opportunity_id.user_id != self.user_id:
            raise ValidationError(_('The Salesperson of the Sale Order and '
                                    'the Opportunity must be the same'))

    @api.constrains('opportunity_id', 'team_id')
    def _check_sales_team(self):
        if self.opportunity_id and self.opportunity_id.team_id and \
                self.opportunity_id.team_id != self.team_id:
            raise ValidationError(_('The Sales Channel of the Sale Order and '
                                    'the Opportunity must be the same'))
