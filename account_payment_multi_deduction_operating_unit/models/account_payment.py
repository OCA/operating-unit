# Copyright 2023 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo import models


class AccountPayment(models.Model):
    _inherit = "account.payment"

    def _get_update_key_list(self):
        res = super()._get_update_key_list()
        return res + ["operating_unit_id"]
