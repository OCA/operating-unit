# Copyright 2021 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class PurchaseAdvancePaymentInv(models.TransientModel):
    _inherit = "purchase.advance.payment.inv"

    def _prepare_deposit_val(self, order, po_line, amount):
        deposit_val = super()._prepare_deposit_val(order, po_line, amount)
        deposit_val["operating_unit_id"] = order.operating_unit_id.id
        return deposit_val
