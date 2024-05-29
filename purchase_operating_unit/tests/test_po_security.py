# Copyright 2015-17 ForgeFlow S.L.
# - Jordi Ballester Alomar
# Copyright 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from . import test_purchase_operating_unit as test_po_ou  # noqa


class TestPoSecurity(test_po_ou.TestPurchaseOperatingUnit):
    def test_po_ou_security(self):
        """Test Security of Purchase Operating Unit"""
        # User 2 is only assigned to Operating Unit 2, and cannot list
        # purchase orders from Operating Unit 1.
        po_ids = (
            self.PurchaseOrder.with_user(self.user2)
            .search([("operating_unit_id", "=", self.ou1.id)])
            .ids
        )
        self.assertEqual(po_ids, [])
        invoice = self._create_invoice(self.purchase1.with_user(self.user1))
        # User 2 cannot list the invoice that was created from PO 1
        invoice_ids = (
            self.AccountInvoice.with_user(self.user2)
            .search([("id", "=", invoice.id)])
            .ids
        )
        self.assertEqual(invoice_ids, [])
        # User 1 is assigned to Operating Unit 1, and can list
        # the purchase order 1 from Operating Unit 1.
        po_ids = (
            self.PurchaseOrder.with_user(self.user1)
            .search([("operating_unit_id", "=", self.ou1.id)])
            .ids
        )
        self.assertNotEqual(po_ids, [])
        # User 1 can list the invoice that was created from PO 2
        invoice_ids = (
            self.AccountInvoice.with_user(self.user1)
            .search([("id", "=", invoice.id)])
            .ids
        )
        self.assertNotEqual(invoice_ids, [])
