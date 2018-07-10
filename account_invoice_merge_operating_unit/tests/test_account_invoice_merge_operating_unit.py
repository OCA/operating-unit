# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# Copyright 2017 Serpent Consulting Services Pvt. Ltd.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.tests import common
from odoo.exceptions import UserError


class TestInvoiceMergeOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestInvoiceMergeOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.invoice_model = self.env['account.invoice']
        self.account_model = self.env['account.account']
        self.inv_merge_model = self.env['invoice.merge']

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

#         Create user1
        self.user_id = self.res_users_model.with_context({
            'no_reset_password': True
        }).create({'name': 'Test Account User',
                   'login': 'user_1',
                   'password': 'demo',
                   'email': 'example@yourcompany.com',
                   'company_id': self.company.id,
                   'company_ids': [(4, self.company.id)],
                   'operating_unit_ids': [(4, self.b2b.id), (4, self.b2c.id)],
                   'groups_id': [(6, 0, [self.grp_acc_manager.id])]
                   })

    def _prepare_invoice(self, operating_unit_id, qty):
        line_products = [(self.product1, qty)]
        # Prepare invoice lines
        lines = []
        acc_type = self.env.ref('account.data_account_type_revenue')
        account_id = self.account_model.search([('user_type_id', '=',
                                                 acc_type.id)], limit=1)
        for product, qty in line_products:
            line_values = {
                'name': product.name,
                'product_id': product.id,
                'quantity': qty,
                'price_unit': 50,
                'account_id': account_id.id
            }
            lines.append((0, 0, line_values))
        inv_vals = {
            'partner_id': self.partner1.id,
            'account_id': self.partner1.property_account_receivable_id.id,
            'operating_unit_id': operating_unit_id,
            'name': 'Test Supplier Invoice',
            'reference_type': 'none',
            'type': 'out_invoice',
            'invoice_line_ids': lines,
        }
        return inv_vals

    def test_invoice_merge_with_opearting_unit(self):
        """Create the invoice and assert the value of
        Operating Unit in the new Invoice.
        """
        # Create invoice
        self.invoice = self.invoice_model.sudo(self.user_id.id).\
            create(self._prepare_invoice(self.b2b.id, 10))

        # Create second invoice with different quantity
        self.invoice2 = self.invoice_model.sudo(self.user_id.id).\
            create(self._prepare_invoice(self.b2b.id, 20))

        wiz_invoice_merge = self.inv_merge_model.with_context({
            'active_ids': [self.invoice.id, self.invoice2.id],
            'active_model': 'account.invoice'
        })

        action = wiz_invoice_merge.create({
            'keep_references': True
        }).merge_invoices()
        invoices = self.invoice_model.browse(action['domain'][0][2])
        self.assertEqual(invoices[1].operating_unit_id,
                         invoices[2].operating_unit_id,
                         'Invoice should have Operating Unit')

    def test_invoice_dirty_check_on_opearting_unit(self):
        """Creates the invoice and asserts that Operating Unit
        of the invoice getting merged are same otherwise
        raise an exception.
        """
        # Create invoice
        self.invoice = self.invoice_model.sudo(self.user_id.id).\
            create(self._prepare_invoice(self.b2b.id, 10))
        # Create second invoice with different quantity
        self.invoice2 = self.invoice_model.sudo(self.user_id.id).\
            create(self._prepare_invoice(self.b2c.id, 20))

        # dirty check to assert similar Operating Unit in invoices

        wiz_invoice_merge = self.inv_merge_model.with_context({
            'active_ids': [self.invoice.id, self.invoice2.id],
            'active_model': 'account.invoice'
        })

        with self.assertRaises(UserError):

            wiz_invoice_merge.create({'keep_references': True})._dirty_check()

        wiz_invoice_merge_dif = self.inv_merge_model.with_context({
            'active_ids': [self.invoice.id, self.invoice2.id],
            'active_model': 'invoice.merge'
        })
        wiz_invoice_merge_dif.create({'keep_references': True})._dirty_check()
