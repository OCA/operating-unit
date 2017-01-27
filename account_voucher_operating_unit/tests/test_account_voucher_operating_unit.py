# -*- coding: utf-8 -*-
# © 2015-17 Eficent
# - Jordi Ballester Alomar
# © 2015 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import common
from datetime import date


class TestAccountVoucherOperatingUnit(common.TransactionCase):

    # Setup 2 invoices,  1st invoice is created for Main OU
    #                    2nd invoice is created for B2C
    # Validate invoices
    # In Customer receipt,
    #    user_all that have access to both OU, will get 2 line.
    #    user_b2c that have access to B2C will get 1 line.
    # Use user_1 to make receipt
    # Check journal enteries

    def setUp(self):
        super(TestAccountVoucherOperatingUnit, self).setUp()
        self.ResUsers = self.env['res.users']
        self.Move = self.env['account.move']
        self.Account = self.env['account.account']
        self.AccountType = self.env['account.account.type']
        self.Voucher = self.env['account.voucher']
        self.VoucherLine = self.env['account.voucher.line']
        self.AccountJournal = self.env['account.journal']
        self.AccountAccount = self.env['account.account']
        self.AccountType = self.env['account.account.type']
        self.OU = self.env['operating.unit']
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
        # receipt journal
        self.utype = self.AccountType.search([('name', '=', 'Income')])
        self.account_rec = self.AccountAccount.search(
            [('name', '=', 'Account Receivable')])
        self.account1 = self._create_account(self.company1.id,
                                             self.utype.id, 'code1')
        self.account2 = self._create_account(self.company1.id,
                                             self.utype.id, 'code2')
        self.journal1 = self._create_journal(self.company1.id,
                                             self.account1,
                                             self.account1, 'code1')
        self.journal2 = self._create_journal(self.company1.id,
                                             self.account2,
                                             self.account2, 'code2')
        # Create users
        self.user_all_id = self._create_user('user_all',
                                             [self.group_account_user],
                                             self.company1,
                                             [self.ou1, self.b2c])
        self.user_b2c_id = self._create_user('user_b2c',
                                             [self.group_account_user],
                                             self.company1,
                                             [self.b2c])

        # user_b2c to create Customer receipt
        self.receipt1 = self._create_customer_receipt(self.ou1, self.journal1)
        self.receipt2 = self._create_customer_receipt(self.b2c, self.journal2)
        self._create_receipt_line(self.receipt1.id)
        self._create_receipt_line(self.receipt2.id)

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

    def _create_journal(self, company, accdeb, acccre, code):

        journal = self.AccountJournal.create({
            'name': 'sales journal',
            'type': 'sale',
            'company_id': company,
            'code': code,
            'default_debit_account_id': accdeb,
            'default_credit_account_id': acccre})
        return journal.id

    def _create_account(self, company, utype, code):

        account = self.AccountAccount.create({
            'name': 'sales account',
            'user_type_id': utype,
            'company_id': company,
            'code': code})
        return account.id

    def _create_customer_receipt(self, operating_unit, journal):
        """Create receipt"""
        rec_vals = {
            'voucher_type': 'sale',
            'account_id': self.account_rec.id,
            'company_id': self.company1.id,
            'journal_id': journal,
            'name': 'Customer receipt: %s' % operating_unit.name,
            'partner_id': self.partner1.id,
            'date': date.today(),
            'operating_unit_id': operating_unit.id,
        }
        # Create receipt
        receipt = self.Voucher.create(rec_vals)
        return receipt

    def _create_receipt_line(self, voucher_id):
        """Create receipt"""
        rec_vals = {
            'product_id': self.product1.id,
            'voucher_id': voucher_id,
            'name': self.product1.name,
            'quantity': 100,
            'price_unit': 100,
            'account_id': 17
        }
        # Create receipt
        line = self.VoucherLine.create(rec_vals)
        return line
