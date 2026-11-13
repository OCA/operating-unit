# Copyright 2015-17 ForgeFlow S.L.
# - Jordi Ballester Alomar
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# © 2026-27 CIT Services - Solomon Prabu
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import fields
from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tests import Form
from odoo.tools import mute_logger

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestPurchaseOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.PurchaseOrder = cls.env["purchase.order"]
        cls.AccountInvoice = cls.env["account.move"]
        cls.AccountAccount = cls.env["account.account"]
        # groups
        cls.group_purchase_user = cls.env.ref("purchase.group_purchase_user")
        # Products
        cls.product1 = cls.env["product.product"].create(
            {"name": "Product 1", "type": "consu"}
        )
        cls.product2 = cls.env["product.product"].create(
            {"name": "Product 2", "type": "consu"}
        )
        cls.product3 = cls.env["product.product"].create(
            {"name": "Product 3", "type": "consu"}
        )
        (cls.product1 | cls.product2).write({"purchase_method": "purchase"})
        # Account
        cls.account = cls.AccountAccount.search(
            [("account_type", "=", "liability_payable")], limit=1
        )
        # Update users
        cls.user1.write(
            {
                "group_ids": [
                    Command.link(cls.group_purchase_user.id),
                ],
            }
        )
        cls.user2.write(
            {
                "group_ids": [
                    Command.link(cls.group_purchase_user.id),
                ],
                "operating_unit_ids": [Command.set([cls.b2b.id])],
            }
        )
        cls.partner1 = cls.env["res.partner"].create({"name": "Partner 1"})
        cls.purchase1 = cls._create_purchase(
            cls.user1,
            [(cls.product1, 1000), (cls.product2, 500), (cls.product3, 800)],
        )
        cls.purchase1.with_user(cls.user1).button_confirm()

    @classmethod
    def _create_purchase(cls, user_id, line_products):
        """Create a purchase order.
        ``line_products`` is a list of tuple [(product, qty)]
        """
        lines = []
        for product, qty in line_products:
            line_values = {
                "name": product.name,
                "product_id": product.id,
                "product_qty": qty,
                "qty_received_manual": qty,
                "uom_id": product.uom_id.id,
                "price_unit": 50,
                "date_planned": fields.Datetime.now(),
            }
            lines.append(Command.create(line_values))
        purchase = cls.PurchaseOrder.with_user(user_id).create(
            {
                "operating_unit_id": cls.ou1.id,
                "requesting_operating_unit_id": cls.ou1.id,
                "partner_id": cls.partner1.id,
                "order_line": lines,
                "company_id": cls.company.id,
            }
        )
        return purchase

    @classmethod
    def _create_invoice(cls, purchase):
        """Create a vendor invoice for the purchase order."""
        purchase.action_create_invoice()
        return purchase.invoice_ids

    def test_01_purchase_operating_unit(self):
        self.purchase1.button_cancel()
        self.purchase1.button_draft()
        # Check change operating unit in purchase
        with self.assertRaises(ValidationError):
            self.b2b.company_id = self.company_2
            with Form(self.purchase1) as po:
                po.operating_unit_id = self.b2b
        self.purchase1.with_user(self.user1).button_confirm()
        invoice = self._create_invoice(self.purchase1)
        self.assertEqual(invoice.operating_unit_id, self.purchase1.operating_unit_id)
        self.assertEqual(
            invoice.invoice_line_ids[0].operating_unit_id,
            invoice.invoice_line_ids[0].purchase_line_id.operating_unit_id,
        )
        # Check change operating unit in invoice line != purchase line,
        # it should error.
        with (
            self.assertRaises(ValidationError),
            Form(invoice.invoice_line_ids[0]) as line,
        ):
            line.operating_unit_id = self.b2b

    def test_02_purchase_report(self):
        """Test the purchase report with operating unit."""
        # Generate the report to trigger the _select and _group_by methods
        report = self.env["purchase.report"]
        # Read records with a filter on operating unit to force using the custom methods
        report_records = report.search([("operating_unit_id", "=", self.ou1.id)])

        # Verify that records exist with the correct operating unit
        self.assertTrue(report_records, "Purchase report should contain records")
        # If records exist, verify at least one has the expected operating unit
        if report_records:
            self.assertEqual(
                report_records[0].operating_unit_id,
                self.ou1,
                "Purchase report record should have the correct operating unit",
            )

    def test_03_vendor_bill_auto_complete(self):
        """Auto-completing a draft vendor bill from a PO takes its OU."""
        move_form = Form(
            self.AccountInvoice.with_context(default_move_type="in_invoice")
        )
        move_form.partner_id = self.partner1
        with mute_logger("odoo.tests.form.onchange"):
            move_form.purchase_vendor_bill_id = self.env["purchase.bill.union"].browse(
                -self.purchase1.id
            )
        invoice = move_form.save()
        self.assertEqual(invoice.operating_unit_id, self.ou1)
        self.assertEqual(
            invoice.invoice_line_ids.purchase_line_id, self.purchase1.order_line
        )
        self.assertEqual(invoice.invoice_line_ids.operating_unit_id, self.ou1)

    def test_04_po_line_and_report_security(self):
        """Users only see PO lines and report rows of their OUs."""
        domain = [("order_id", "=", self.purchase1.id)]
        self.assertFalse(
            self.env["purchase.order.line"].with_user(self.user2).search(domain)
        )
        self.assertEqual(
            self.env["purchase.order.line"].with_user(self.user1).search(domain),
            self.purchase1.order_line,
        )
        self.assertFalse(
            self.env["purchase.report"].with_user(self.user2).search(domain)
        )
        self.assertTrue(
            self.env["purchase.report"].with_user(self.user1).search(domain)
        )

    def test_05_default_operating_unit(self):
        """A new PO takes the default OU of the user who creates it."""
        self.user2.default_operating_unit_id = self.b2b
        purchase = self.PurchaseOrder.with_user(self.user2).create(
            {"partner_id": self.partner1.id}
        )
        self.assertEqual(purchase.operating_unit_id, self.b2b)
        self.assertEqual(purchase.requesting_operating_unit_id, self.b2b)
