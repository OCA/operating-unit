# -*- coding: utf-8 -*-
# © 2016-17 Eficent Business and IT Consulting Services S.L.
# © 2016 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from . import test_account_operating_unit as test_ou


class TestInvoiceOperatingUnit(test_ou.TestAccountOperatingUnit):

    def test_create_invoice_validate(self):
        """Create & Validate the invoice.
        Test that when an invoice is created, the operating unit is
        passed to the accounting journal items.
        """
        # Create invoice
        self.invoice =\
            self.invoice_model.sudo(self.user_id.id).create(
                self._prepare_invoice(self.b2b.id))
        # Validate the invoice
        self.invoice.sudo(self.user_id.id).action_invoice_open()
        # Check Operating Units in journal entries
        all_op_units = all(move_line.operating_unit_id.id == self.b2b.id for
                           move_line in self.invoice.move_id.line_ids)
        # Assert if journal entries of the invoice
        # have different operating units
        self.assertNotEqual(all_op_units, False, 'Journal Entries have\
                            different Operating Units.')
