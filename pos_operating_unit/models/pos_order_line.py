# Copyright 2022 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Operating Unit",
        readonly=True,
    )

    def _order_line_fields(self, line, session_id=None):
        res = super()._order_line_fields(line, session_id)
        session = (
            self.env["pos.session"].browse(session_id).exists() if session_id else None
        )
        if session:
            res[2]["operating_unit_id"] = session.operating_unit_id.id
        return res
