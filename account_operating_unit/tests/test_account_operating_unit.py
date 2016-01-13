# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp.addons.account.tests import account_test_classes


class TestAccountOperatingUnit(account_test_classes.AccountingTestCase):

    def setUp(self):
        super(TestAccountOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.aml_model = self.env['account.move.line']
        self.account_model = self.env['account.account']
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
        self.product3 = self.env.ref('product.product_product_11')
        # Create user1
        self.user_id =\
            self.res_users_model.with_context({'no_reset_password': True}).\
            create({
                'name': 'Test Account User',
                'login': 'user_1',
                'password': 'demo',
                'email': 'example@yourcompany.com',
                'company_id': self.company.id,
                'company_ids': [(4, self.company.id)],
                'operating_unit_ids': [(4, self.b2b.id), (4, self.b2c.id)],
                'groups_id': [(6, 0, [self.grp_acc_manager.id])]
            })
        # Create cash - test account
        user_type = self.env.ref('account.data_account_type_liquidity')
        self.cash_account_id = self.account_model.create({
            'name': 'Cash - Test',
            'code': 'test_cash',
            'user_type_id': user_type.id,
            'company_id': self.company.id,
        })
        # Create Inter-OU Clearing - test account
        user_type = self.env.ref('account.data_account_type_equity')
        self.inter_ou_account_id = self.account_model.create({
            'name': 'Inter-OU Clearing',
            'code': 'test_inter_ou',
            'user_type_id': user_type.id,
            'company_id': self.company.id,
        })
        # Assign the Inter-OU Clearing account to the company
        self.company.inter_ou_clearing_account_id = self.inter_ou_account_id.id
        self.company.ou_is_self_balanced = self.ou_is_self_balanced.id

        # Create user2
        self.user2_id =\
            self.res_users_model.with_context({'no_reset_password': True}).\
            create({
                'name': 'Test Account User',
                'login': 'user_2',
                'password': 'demo',
                'email': 'example@yourcompany.com',
                'company_id': self.company.id,
                'company_ids': [(4, self.company.id)],
                'operating_unit_ids': [(4, self.b2c.id)],
                'groups_id': [(6, 0, [self.grp_acc_manager.id])]
            })
