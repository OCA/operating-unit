# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# © 2026-27 CIT Services - Solomon Prabu
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class PurchaseReport(models.Model):
    _inherit = "purchase.report"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        readonly=True,
    )

    def _select_list(self, table):
        return [*super()._select_list(table), table.order_id.operating_unit_id]
