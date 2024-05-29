# Copyright 2015-17 ForgeFlow S.L.
# - Jordi Ballester Alomar
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import time

from odoo.exceptions import ValidationError
from odoo.models import Command
from odoo.tests import Form
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT

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
        cls.product1 = cls.env.ref("product.product_product_7")
        cls.product2 = cls.env.ref("product.product_product_9")
        cls.product3 = cls.env.ref("product.product_product_11")
        (cls.product1 | cls.product2).write({"purchase_method": "purchase"})
        # Account
        cls.account = cls.AccountAccount.search(
            [("account_type", "=", "liability_payable")], limit=1
        )
        # Update users
        cls.user1.write(
            {
                "groups_id": [
                    Command.link(cls.group_purchase_user.id),
                ],
            }
        )
        cls.user2.write(
            {
                "groups_id": [
                    Command.link(cls.group_purchase_user.id),
                ],
                "operating_unit_ids": [Command.set([cls.b2b.id])],
            }
        )
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
                "product_uom": product.uom_id.id,
                "price_unit": 50,
                "date_planned": time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
            }
            lines.append((0, 0, line_values))
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
        with self.assertRaises(ValidationError):
            with Form(invoice.invoice_line_ids[0]) as line:
                line.operating_unit_id = self.b2b
