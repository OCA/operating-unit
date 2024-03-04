# Copyright 2015-17 ForgeFlow S.L.
# - Jordi Ballester Alomar
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import time

from odoo.exceptions import AccessError, ValidationError
from odoo.tests import Form, common
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class TestPurchaseOperatingUnit(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ResUsers = cls.env["res.users"]
        cls.PurchaseOrder = cls.env["purchase.order"]
        cls.AccountInvoice = cls.env["account.move"]
        cls.AccountAccount = cls.env["account.account"]
        # company
        cls.company = cls.env.ref("base.main_company")
        # groups
        cls.group_purchase_user = cls.env.ref("purchase.group_purchase_user")
        cls.group_operating_unit = cls.env.ref(
            "operating_unit.group_multi_operating_unit"
        )
        # Main Operating Unit
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        # B2B Operating Unit
        cls.b2b = cls.env.ref("operating_unit.b2b_operating_unit")
        # Partner
        cls.partner1 = cls.env.ref("base.res_partner_1")
        # Products
        cls.product1 = cls.env.ref("product.product_product_7")
        cls.product2 = cls.env.ref("product.product_product_9")
        cls.product3 = cls.env.ref("product.product_product_11")
        # Account
        # payable_acc_type = cls.env.ref("account.data_account_type_payable").id
        cls.account = cls.AccountAccount.search(
            [("account_type", "=", "liability_payable")], limit=1
        )
        # Create users
        cls.user1_id = cls._create_user(
            "user_1",
            [cls.group_purchase_user, cls.group_operating_unit],
            cls.company,
            [cls.ou1],
        )
        cls.user2_id = cls._create_user(
            "user_2",
            [cls.group_purchase_user],
            cls.company,
            [cls.b2b],
        )
        cls.purchase1 = cls._create_purchase(
            cls.user1_id,
            [(cls.product1, 1000), (cls.product2, 500), (cls.product3, 800)],
        )
        cls.purchase1.with_user(cls.user1_id).button_confirm()
        cls.purchase1.order_line[0].qty_received = cls.purchase1.order_line[
            0
        ].product_qty
        cls.purchase1.with_user(cls.user1_id).action_create_invoice()
        # cls.invoice = cls._create_invoice(cls.purchase1, cls.partner1, cls.account)
        cls.invoice = cls.purchase1.invoice_ids[0]

    @classmethod
    def _create_user(cls, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = cls.ResUsers.with_context(**{"no_reset_password": True}).create(
            {
                "name": "Chicago Purchase User",
                "login": login,
                "password": "demo",
                "email": "chicago@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user.id

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
    def _create_invoice(cls, purchase, partner, account):
        """Create a vendor invoice for the purchase order."""
        invoice_vals = {
            "purchase_id": purchase.id,
            "partner_id": partner.id,
            "move_type": "in_invoice",
        }
        purchase_context = {
            "active_id": purchase.id,
            "active_ids": purchase.ids,
            "active_model": "purchase.order",
        }
        res = (
            cls.env["account.move"]
            .with_context(**purchase_context)
            .create(invoice_vals)
        )
        return res

    def test_01_purchase_operating_unit(self):
        self.purchase1.button_cancel()
        self.purchase1.button_draft()
        # Check change operating unit in purchase
        with self.assertRaises(ValidationError):
            self.b2b.company_id = False
            # The user_1 is used here so he's able to see the field operating_unit
            with Form(self.purchase1.with_user(self.user1_id)) as po:
                po.operating_unit_id = self.b2b
        # This has been changed to follow the standard flow of creating a
        # purchase order and then billing
        self.purchase1.with_user(self.user1_id).button_confirm()
        # self.purchase1.order_line[0].qty_received = self.purchase1.order_line[0].product_qty
        # self.purchase1.with_user(self.user1_id).action_create_invoice()
        # Create Vendor Bill
        # The user_1 is used here so he's able to see the field purchase_id
        # f = Form(self.env["account.move"].with_context(
        # default_move_type="in_invoice").with_user(self.user1_id))
        # f.partner_id = self.purchase1.partner_id
        # f.purchase_id = self.purchase1
        # invoice = f.save()

        self.assertEqual(
            self.purchase1.invoice_ids[0].operating_unit_id,
            self.purchase1.operating_unit_id,
        )
        self.assertEqual(
            self.purchase1.invoice_ids[0].invoice_line_ids[0].operating_unit_id,
            self.purchase1.invoice_ids[0]
            .invoice_line_ids[0]
            .purchase_line_id.operating_unit_id,
        )
        # Check change operating unit in invoice line != purchase line,
        # it should error.
        with self.assertRaises(AccessError):
            with Form(self.purchase1.invoice_ids[0].invoice_line_ids[0]) as line:
                line.operating_unit_id = self.b2b
