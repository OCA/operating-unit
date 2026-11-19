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
        self.invoice = self.move_model.with_user(self.user1.id).create(
            self._prepare_invoice(self.b2b.id)
        )
        self.invoice.invoice_date = self.invoice.date
        # Validate the invoice
        self.invoice.with_user(self.user1.id).action_post()
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
        # Invoice without OU: suitable_journal_ids returns all company journals
        invoice_no_ou = self.move_model.create(
            {"partner_id": self.partner1.id, "move_type": "in_invoice"}
        )
        self.assertTrue(invoice_no_ou.suitable_journal_ids)

    def test_operating_unit_lock_date(self):
        """The operating unit of a posted entry can't change in a locked period."""
        invoice = self.move_model.with_user(self.user1.id).create(
            self._prepare_invoice(self.b2b.id)
        )
        invoice.invoice_date = "2019-01-15"
        invoice.action_post()

        def write_operating_unit(operating_unit):
            invoice.operating_unit_id = operating_unit
            invoice.line_ids.operating_unit_id = operating_unit

        write_operating_unit(self.b2c)
        self.assertEqual(invoice.line_ids.operating_unit_id, self.b2c)
        self.company.fiscalyear_lock_date = "2019-01-31"
        with self.assertRaisesRegex(UserError, "prior to and inclusive of"):
            write_operating_unit(self.b2b)

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

        # Ensure user has the correct operating unit
        self.user1.write({"operating_unit_ids": [(4, self.ou1.id)]})

        # Open the form with default operating unit context
        with Form(
            self.env["account.move"].with_context(
                default_operating_unit_id=self.ou1.id, default_move_type="out_invoice"
            )
        ) as invoice_form:
            # Check the default operating unit in the form
            self.assertEqual(invoice_form.operating_unit_id, self.ou1)

            # Copy OU1 journal and validate operating unit
            ou1_journal = invoice_form.journal_id.copy(
                {"operating_unit_id": self.ou1.id, "company_id": self.company.id}
            )
            # Update operating unit and journal in the form
            invoice_form.operating_unit_id = self.b2b
            self.assertEqual(invoice_form.journal_id, journal_b2b)

            invoice_form.journal_id = ou1_journal
            self.assertEqual(invoice_form.operating_unit_id, self.ou1)

    def test_journal_auto_switches_when_ou_changes(self):
        """
        When the operating unit is changed on an invoice, the journal is
        automatically replaced with one that matches the new operating unit.
        """
        ou1_sale_journal = self.journal_model.create(
            {
                "name": "OU1 Sale",
                "code": "OU1S",
                "type": "sale",
                "operating_unit_id": self.ou1.id,
                "company_id": self.company.id,
            }
        )
        b2b_sale_journal = self.journal_model.create(
            {
                "name": "B2B Sale",
                "code": "B2BS",
                "type": "sale",
                "operating_unit_id": self.b2b.id,
                "company_id": self.company.id,
            }
        )
        invoice = self.move_model.create(
            {
                "partner_id": self.partner1.id,
                "move_type": "out_invoice",
                "operating_unit_id": self.b2b.id,
                "journal_id": b2b_sale_journal.id,
            }
        )
        with Form(invoice) as inv_form:
            inv_form.operating_unit_id = self.ou1
            self.assertEqual(inv_form.journal_id, ou1_sale_journal)
