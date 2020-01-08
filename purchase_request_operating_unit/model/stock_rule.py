# Copyright 2015-19 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models


class StockRule(models.Model):
    _inherit = 'stock.rule'

    @api.model
    def _prepare_purchase_request(self, origin, values):
        res = super(StockRule, self)._prepare_purchase_request(origin, values)
        res.update({
            'operating_unit_id': values.get('operating_unit_id', False),
        })
        return res
