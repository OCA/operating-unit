# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp.tests import common
from datetime import date


class TestAccountVoucherOperatingUnit(common.TransactionCase):

    # Setup 2 invoices,  1st invoice is created for Main OU
    #                    2nd invoice is created for B2C
    # Validate invoices
    # In Customer Payment,
    #    user_all that have access to both OU, will get 2 line.
    #    user_b2c that have access to B2C will get 1 line.
    # Use user_1 to make payment
    # Check journal enteries

    def setUp(self):
        super(TestAccountVoucherOperatingUnit, self).setUp()
        self.ResUsers = self.env['res.users']
        self.Invoice = self.env['account.invoice']
        self.InvoiceLine = self.env['account.invoice.line']
        self.Account = self.env['account.account']
        self.AccountType = self.env['account.account.type']
        self.Voucher = self.env['account.voucher']
        # company
        self.company1 = self.env.ref('base.main_company')
        # groups
        self.group_account_user = self.env.ref('account.group_account_user')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # Partner
        self.partner1 = self.env.ref('base.res_partner_1')
        # Products
        self.product1 = self.env.ref('product.product_product_7')
        self.product2 = self.env.ref('product.product_product_9')
        self.product3 = self.env.ref('product.product_product_11')
        # Payment journal
        self.payment_journal = self.env.ref('account.bank_journal')
        self.payment_account = self.env.ref('account.bnk')
        # Create users
        self.user_all_id = self._create_user('user_all',
                                             [self.group_account_user],
                                             self.company1,
                                             [self.ou1, self.b2c])
        self.user_b2c_id = self._create_user('user_b2c',
                                             [self.group_account_user],
                                             self.company1,
                                             [self.b2c])
        # Create Invoice with Main Operating Unit
        self.invoice_ou = self._create_invoice(self.ou1.id)
        # Create Invoice with B2C
        self.invoice_b2c = self._create_invoice(self.b2c.id)

        # user_b2c to create Customer Payment
        self.payment = self._create_customer_payment(
            self.user_all_id, self.ou1.id, self.partner1.id)

    def _create_user(self, login, groups, company, operating_units):
        """ Create a user."""
        group_ids = [group.id for group in groups]
        user =\
            self.ResUsers.with_context({'no_reset_password': True}).\
            create({
                'name': 'Budget User',
                'login': login,
                'password': 'demo',
                'email': 'chicago@yourcompany.com',
                'company_id': company.id,
                'company_ids': [(4, company.id)],
                'operating_unit_ids': [(4, ou.id) for ou in operating_units],
                'groups_id': [(6, 0, group_ids)]
            })
        return user.id

    def _create_invoice(self, operating_unit_id):
        """Create & Validate the invoice."""
        line_products = [(self.product1, 2)]
        # Prepare invoice lines
        lines = []
        user_types = self.AccountType.search([('code', '=', 'expense')])
        user_type_id = user_types and user_types[0].id or False
        for product, qty in line_products:
            line_values = {
                'name': product.name,
                'product_id': product.id,
                'quantity': qty,
                'price_unit': 100,
                'account_id': self.Account.search(
                    [('user_type', '=', user_type_id)], limit=1).id,
            }
            lines.append((0, 0, line_values))
        inv_vals = {
            'partner_id': self.partner1.id,
            'account_id': self.partner1.property_account_payable.id,
            'operating_unit_id': operating_unit_id,
            'name': "Customer Invoice (Main OU)",
            'reference_type': "none",
            'type': 'out_invoice',
            'invoice_line': lines,
        }
        # Create invoice
        self.invoice =\
            self.Invoice.sudo(self.user_all_id).create(inv_vals)
        # Validate the invoice
        self.invoice.sudo(self.user_all_id).signal_workflow('invoice_open')
        return self.invoice

    def _create_customer_payment(self, user_id, operating_unit_id, partner_id):
        """Create & Validate the invoice."""
        pay_vals = {
            'type': 'payment',
            'account_id': self.payment_account.id,
            'amount': 0.0,
            'company_id': self.company1.id,
            'journal_id': self.payment_journal.id,
            'name': 'Customer Payment: B2C',
            'partner_id': self.partner1.id,
            'date': date.today(),
            'operating_unit_id': operating_unit_id,
        }
        # Create invoice
        self.payment =\
            self.Voucher.sudo(user_id).create(pay_vals)
        return self.payment
