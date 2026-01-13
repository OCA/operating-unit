# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import tests
from odoo.tools.safe_eval import safe_eval

from . import test_account_operating_unit as test_ou


@tests.tagged("post_install", "-at_install")
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

    def test_manager_select_operating_unit(self):
        """A Manager of Operating Units can
        assign any Operating Unit to an invoice."""
        # Arrange
        manager_user = self.ou_manager_user
        # pre-condition
        self.assertTrue(manager_user.has_group(self.grp_ou_manager_xmlid))

        # Act
        invoice_form = tests.Form(self.move_model.with_user(manager_user.id))
        invoice = invoice_form.save()

        # Assert
        invoice_form_OU_field = invoice_form._view["fields"]["operating_unit_id"]
        selectable_OUs_domain = safe_eval(
            invoice_form_OU_field.get("domain") or "[]",
            globals_dict=dict(
                invoice.read()[0],
                uid=invoice.env.uid,
            ),
        )
        selectable_OUs = (
            self.env["operating.unit"]
            .with_user(manager_user.id)
            .search(selectable_OUs_domain)
        )
        manager_OUs = manager_user.with_company(invoice.company_id).operating_unit_ids
        self.assertEqual(manager_OUs, selectable_OUs)
