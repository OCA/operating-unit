# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.addons.account_voucher_operating_unit.tests import\
    test_account_voucher_operating_unit as test_ou


class TestPaymentOU(test_ou.TestAccountVoucherOperatingUnit):

    def test_create_customer_payment(self):
        """ Test Create Payment of Voucher Operating Unit """
        # user_b2c, on customer payment, show only invoices on B2C
        amount = 300
        rate = self.payment.payment_rate
        partner_id = self.payment.partner_id.id
        journal_id = self.payment.journal_id.id
        currency_id = self.payment.currency_id.id
        ttype = self.payment.type
        date = self.payment.date
        payment_rate_currency_id = self.payment.payment_rate_currency_id.id
        company_id = self.payment.company_id.id

        # user_all will see both Main OU and B2C invoices (2 records)
        res = self.payment.sudo(self.user_all_id).onchange_amount(
            amount, rate, partner_id, journal_id, currency_id, ttype, date,
            payment_rate_currency_id, company_id)
        self.assertEqual(len(res['value']['line_cr_ids']), 2)

        # user_b2c will see only B2C invoices (1 records)
        res = self.payment.sudo(self.user_b2c_id).onchange_amount(
            amount, rate, partner_id, journal_id, currency_id, ttype, date,
            payment_rate_currency_id, company_id)
        self.assertEqual(len(res['value']['line_cr_ids']), 1)
