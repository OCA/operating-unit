# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. -
# Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.tests import common
from openerp.exceptions import ValidationError


class TestPurchaseRequisitionOperatingUnit(common.TransactionCase):

    # Test Cases:
    # - Create Purchase Requisition
    #   - Change operating_unit_id will change picking_type_id correctly
    #   - User can't use picking_type_id not belong to same operating_unit_id
    # - When create PO, the OU and picking_type_id will be pass correctly

    def setUp(self):
        super(TestPurchaseRequisitionOperatingUnit, self).setUp()
        self.pr_model = self.env['purchase.requisition']
        self.pr_line_model = self.env['purchase.requisition.line']
        self.po_model = self.env['purchase.order']
        # company
        self.company = self.env.ref('base.main_company')
        self.grp_acc_manager = self.env.ref('account.group_account_manager')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2B Operating Unit
        self.b2b = self.env.ref('operating_unit.b2b_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # Partner
        self.partner1 = self.env.ref('base.res_partner_1')
        # Products
        self.product1 = self.env.ref('product.product_product_7')
        self.product2 = self.env.ref('product.product_product_9')

    def _create_pr(self):
        line_products = [(self.product1, 1000),
                         (self.product2, 500), ]
        lines = []
        for product, qty in line_products:
            line_values = {
                'product_id': product.id,
                'product_qty': qty,
            }
            lines.append((0, 0, line_values))
        pr_vals = {
            'exclusive': 'exclusive',
            'operating_unit_id': self.ou1.id,
            'line_ids': lines,
        }
        # Create PR
        self.pr = self.pr_model.sudo().create(pr_vals)

    def test_create_purchase_requisition(self):
        self._create_pr()
        # Change OU, result in warning
        with self.assertRaises(ValidationError):
            self.pr.operating_unit_id = self.b2c
        # on_change OU
        pr_mock = self.pr_model.new()
        pr_mock.operating_unit_id = self.b2c
        pr_mock._onchange_operating_unit_id()
        picktype = pr_mock.picking_type_id  # on change result
        self.assertEqual(self.b2c, picktype.warehouse_id.operating_unit_id,
                         'Purchase Requisition and the Warehouse of picking '
                         'type does not belong to same Operating Unit.')
        # Now OU and Picking Type should be in line as b2c
        self.pr.picking_type_id = picktype
        # Confirm Call
        self.pr.sudo().signal_workflow('sent_suppliers')
        self.assertEqual(self.pr.state, 'in_progress',
                         'State not changed to Confirmed')
        # Create PO
        pr_po = self.pr.make_purchase_order(self.partner1.id)
        po_id = pr_po.get(self.pr.id)
        self.po = self.po_model.browse(po_id)
        self.assertEqual(self.po.operating_unit_id, self.pr.operating_unit_id,
                         'Operating Unit is not correctly passed to PO')
        self.assertEqual(self.po.picking_type_id, self.pr.picking_type_id,
                         'Picking Type is not correctly passed to PO')
