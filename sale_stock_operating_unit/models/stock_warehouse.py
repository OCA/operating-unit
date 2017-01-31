# -*- coding: utf-8 -*-
# © 2015-17 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models, _
from odoo.exceptions import ValidationError


class StockWarehouse(models.Model):
    _inherit = 'stock.warehouse'

    @api.multi
    @api.constrains('operating_unit_id')
    def _check_existing_so_in_wh(self):
        for rec in self:
            sales = self.env['sales.order'].search([
                ('warehouse_id', '=', rec.id),
                ('operating_unit_id', '!=', rec.operating_unit_id)])
            if sales:
                raise ValidationError(_(
                    'Sales Order records already exist(s) for this warehouse'
                    ' and operating unit.'))
