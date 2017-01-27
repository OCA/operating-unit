# -*- coding: utf-8 -*-
# © 2015-2017 Eficent
# - Jordi Ballester Alomar
# © 2015-2017 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# © 2015-2017 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from datetime import date
from odoo.tests import common


class TestBudgetOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestBudgetOperatingUnit, self).setUp()
        self.ResUsers = self.env['res.users']
        self.BudgetObj = self.env['crossovered.budget']
        self.BudgetLineObj = self.env['crossovered.budget.lines']
        # company
        self.company1 = self.env.ref('base.main_company')
        # groups
        self.group_account_user = self.env.ref('account.group_account_user')
        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')
        # Create users
        self.user1_id = self._create_user('budget_user_1',
                                          [self.group_account_user],
                                          self.company1,
                                          [self.ou1, self.b2c])
        self.user2_id = self._create_user('budget_user_2',
                                          [self.group_account_user],
                                          self.company1,
                                          [self.b2c])
        # Create Main OU budget
        self.budget_ou1 = self._create_budget(self.user1_id,
                                              self.ou1.id,
                                              'Budget Main OU')
        # Create B2C budget
        self.budget_b2c = self._create_budget(self.user2_id,
                                              self.b2c.id,
                                              'Budget B2C')

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

    def _create_budget(self, user_id, ou_id, name):
        """Create a Budget."""
        budget = self.BudgetObj.sudo(user_id).create({
            'name': name,
            'creating_user_id': user_id,
            'operating_unit_id': ou_id,
            'date_from': date.today(),
            'date_to': date.today(),
        })
        return budget
