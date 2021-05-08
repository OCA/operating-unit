# Copyright (C) 2018-Today:
# Dinamiche Aziendali Srl (<http://www.dinamicheaziendali.it/>)
# @author: Giuseppe Borruso <gborruso@dinamicheaziendali.it>
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Operating Unit',
        readonly=True
    )

    requesting_operating_unit_id = fields.Many2one(
        comodel_name='operating.unit',
        string='Requesting Operating Unit',
        readonly=True
    )

    def _select(self):
        res = super()._select()
        res += """
            , s.operating_unit_id AS operating_unit_id
            , s.requesting_operating_unit_id AS requesting_operating_unit_id
        """
        return res

    def _group_by(self):
        res = super()._group_by()
        res += ", s.operating_unit_id, s.requesting_operating_unit_id"
        return res
