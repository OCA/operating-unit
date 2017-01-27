# -*- coding: utf-8 -*-
# © 2015-17 Eficent
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from . import test_account_voucher_operating_unit as test_ou


class TestReceiptOU(test_ou.TestAccountVoucherOperatingUnit):

    def test_create_customer_receipt(self):
        """
        Test Create a Receipt of Voucher Operating Unit
        - Only invoice of the same Operating Unit will be listed.
        - Validate the Account Voucher
        """

        # Validate the voucher
        self.receipt1.proforma_voucher()
        self.receipt2.proforma_voucher()
        # Check Operating Units in journal entries
        all_op_units1 = all(
            move_line.operating_unit_id.id ==
            self.receipt1.operating_unit_id.id
            for move_line in self.receipt1.move_id.line_ids)
        all_op_units2 = all(
            move_line2.operating_unit_id.id ==
            self.receipt2.operating_unit_id.id
            for move_line2 in self.receipt2.move_id.line_ids)
        # Assert if journal entries of the receipt
        # have different operating units
        self.assertNotEqual(all_op_units1, False, 'Journal Entries have\
                            different Operating Units.')
        self.assertNotEqual(all_op_units2, False, 'Journal Entries have\
            different Operating Units.')

        # user_b2c, on customer receipt, show only invoices on B2C
        # user_all will see both Main OU and B2C moves (2 records)
        move1 = self.receipt1.move_id
        move2 = self.receipt2.move_id
        res = self.Move.sudo(self.user_all_id).search(
            [('id', 'in', [move1.id, move2.id])])
        self.assertEqual(len(res), 2)
        # user_b2c will see only B2C invoices (1 records)
        res = self.Move.sudo(self.user_b2c_id).search(
            [('id', 'in', [move1.id, move2.id]),
             ('operating_unit_id', '=', self.b2c.id)])
        self.assertEqual(len(res), 1)
