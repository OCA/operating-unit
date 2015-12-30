# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.addons.account_operating_unit.tests import\
    test_account_operating_unit as test_ou


class TestInvoiceOperatingUnit(test_ou.TestAccountOperatingUnit):

    def test_create_invoice_validate(self):
        """Create & Validate the invoice.
        Test that when an invoice is created, the operating unit is
        passed to the accounting journal items.
        """
        line_products = [(self.product1, 1000),
                         (self.product2, 500),
                         (self.product3, 800)]
        self.invoice_model = self.env['account.invoice']
        self.journal_model = self.env['account.journal']
        self.product_model = self.env['product.product']
        self.inv_line_model = self.env['account.invoice.line']
        # Prepare invoice lines
        lines = []
        acc_type = self.env.ref('account.data_account_type_expenses')
        for product, qty in line_products:
            line_values = {
                'name': product.name,
                'product_id': product.id,
                'quantity': qty,
                'price_unit': 50,
                'account_id': self.env['account.account'].
                search([('user_type_id', '=', acc_type.id)], limit=1).id,
            }
            lines.append((0, 0, line_values))
        inv_vals = {
            'partner_id': self.partner1.id,
            'account_id': self.partner1.property_account_payable_id.id,
            'operating_unit_id': self.b2b.id,
            'name': "Test Supplier Invoice",
            'reference_type': "none",
            'type': 'in_invoice',
            'invoice_line_ids': lines,
        }
        # Create invoice
        self.invoice =\
            self.invoice_model.sudo(self.user_id.id).create(inv_vals)
        # Validate the invoice
        self.invoice.sudo(self.user_id.id).signal_workflow('invoice_open')
        # Check Operating Units in journal entries
        all_op_units = all(move_line.operating_unit_id.id == self.b2b.id for
                           move_line in self.invoice.move_id.line_ids)
        # Assert if journal entries of the invoice
        # have different operating units
        self.assertNotEqual(all_op_units, False, 'Journal Entries have\
                            different Operating Units.')
