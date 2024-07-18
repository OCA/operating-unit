# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.exceptions import UserError
from odoo.tests import Form, tagged

from . import test_account_operating_unit as test_ou


@tagged("post_install", "-at_install")
class TestInvoiceOperatingUnit(test_ou.TestAccountOperatingUnit):
    def test_create_invoice_validate(self):
        """Create & Validate the invoice.
        Test that when an invoice is created, the operating unit is
        passed to the accounting journal items.
        """
        # Create invoice
        self.invoice = self.move_model.with_user(self.user_id.id).create(
            self._prepare_invoice(self.b2b.id)
        )
        self.invoice.invoice_date = self.invoice.date
        # Validate the invoice
        self.invoice.with_user(self.user_id.id).action_post()
        # Check Operating Units in journal entries
        all_op_units = all(
            move_line.operating_unit_id.id == self.b2b.id
            for move_line in self.invoice.line_ids
        )
        # Assert if journal entries of the invoice
        # have different operating units
        self.assertNotEqual(
            all_op_units,
            False,
            "Journal Entries have different Operating Units.",
        )
        # Test change ou in move
        with self.assertRaises(UserError):
            self.invoice.line_ids[0].operating_unit_id = self.b2c.id
        # Test change company in move
        new_company = self.env["res.company"].create({"name": "New Company"})
        with self.assertRaises(UserError):
            self.invoice.line_ids[0].company_id = new_company.id
        # Check report invoice
        self.env["account.invoice.report"].sudo().read_group(
            [], ["operating_unit_id"], ["operating_unit_id"]
        )

    def test_form(self):
        """Test that the UI behaves as expected"""
        journal_b2b = self.env["account.journal"].create(
            {
                "name": "B2B journal",
                "code": "B2B",
                "type": "sale",
                "operating_unit_id": self.b2b.id,
                "company_id": self.company.id,
            }
        )
        with Form(
            self.env["account.move"].with_context(default_move_type="out_invoice")
        ) as invoice_form:
            self.assertEqual(invoice_form.operating_unit_id, self.ou1)
            ou1_journal = invoice_form.journal_id.copy(
                dict(
                    operating_unit_id=self.ou1.id,
                    company_id=self.company.id,
                )
            )
            invoice_form.operating_unit_id = self.b2b
            self.assertEqual(invoice_form.journal_id, journal_b2b)
            invoice_form.journal_id = ou1_journal
            self.assertEqual(invoice_form.operating_unit_id, self.ou1)
