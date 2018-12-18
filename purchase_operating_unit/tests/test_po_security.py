# © 2015-17 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from . import test_purchase_operating_unit as test_po_ou  # noqa


class TestPoSecurity(test_po_ou.TestPurchaseOperatingUnit):

    def test_po_ou_security(self):
        """Test Security of Purchase Operating Unit"""
        # User 2 is only assigned to Operating Unit 2, and cannot list
        # purchase orders from Operating Unit 1.
        po_ids =\
            self.PurchaseOrder.sudo(self.user2_id).\
            search([('operating_unit_id', '=', self.ou1.id)]).ids
        self.assertEqual(po_ids, [])
        # User 2 cannot list the picking that was created from PO 1
        picking_ids =\
            self.StockPicking.sudo(self.user2_id).\
            search([('id', 'in', self.purchase1.picking_ids.ids)]).ids
        self.assertEqual(picking_ids, [])
        # User 2 cannot list the invoice that was created from PO 1
        invoice_ids = self.AccountInvoice.sudo(self.user2_id).\
            search([('purchase_id', '=', self.purchase1.id)]).ids
        self.assertEqual(invoice_ids, [])
        # User 1 is assigned to Operating Unit 1, and can list
        # the purchase order 1 from Operating Unit 1.
        po_ids =\
            self.PurchaseOrder.sudo(self.user1_id).\
            search([('operating_unit_id', '=', self.ou1.id)]).ids
        self.assertNotEqual(po_ids, [])
        # User 1 can list the picking that was created from PO 1
        picking_ids =\
            self.StockPicking.sudo(self.user1_id).\
            search([('id', 'in', self.purchase1.picking_ids.ids)]).ids
        self.assertNotEqual(picking_ids, [])
#        # User 1 can list the invoice that was created from PO 2
        invoice_ids = self.AccountInvoice.sudo(self.user1_id).\
            search([('purchase_id', '=', self.purchase1.id)]).ids
        self.assertNotEqual(invoice_ids, [])
