# Copyright 2020, Jarsa Sistemas, S.A. de C.V.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).


from odoo import fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    purchase_sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Purchase Order Sequence",
        help="Sequence of purchase order with this operating unit",
    )
