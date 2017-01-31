# -*- coding: utf-8 -*-
# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import fields, models


class SaleReport(models.Model):

    _inherit = "sale.report"

    operating_unit_id = fields.Many2one('operating.unit', 'Operating Unit')

    def _select(self):
        select_str = super(SaleReport, self)._select()
        select_str += """
            ,s.operating_unit_id
        """
        return select_str

    def _group_by(self):
        group_by_str = super(SaleReport, self)._group_by()
        group_by_str += """
            ,s.operating_unit_id
        """
        return group_by_str
