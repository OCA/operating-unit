# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    payment_transfer_seq_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Payment Transfer Sequence",
        help="Sequence of payment transfer with this operating unit",
    )
    payment_cust_inv_seq_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Payment Customer Invoice Sequence",
        help="Sequence of payment customer invoice with this operating unit",
    )
    payment_cust_refund_seq_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Payment Customer Refund Sequence",
        help="Sequence of payment customer refund with this operating unit",
    )
    payment_supp_inv_seq_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Payment Suppier Invoice Sequence",
        help="Sequence of payment supplier invoice with this operating unit",
    )
    payment_supp_refund_seq_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Payment Suppier Refund Sequence",
        help="Sequence of payment supplier refund with this operating unit",
    )
