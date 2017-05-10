# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, models
from openerp.exceptions import Warning as UserError
from openerp.tools.translate import _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('opportunity_id', 'operating_unit_id')
    def _check_sale_operating_unit(self):
        if self.opportunity_id and self.opportunity_id.operating_unit_id and\
                self.opportunity_id.\
                operating_unit_id != self.operating_unit_id:
            raise UserError(_('Configuration error!\nThe Operating Unit\
            of Sales Order should be same that of Opportunity.'))
