# -*- coding: utf-8 -*-
# © 2015-2017 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# © 2015-2017 Ecosoft Co. Ltd. - Kitti Upariphutthiphong
# © 2015-2017 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from openerp.addons.account_budget_operating_unit.tests import\
    test_budget_operating_unit as test_budget_ou


class TestBudgetSecurity(test_budget_ou.TestBudgetOperatingUnit):

    def test_budget_ou_security(self):
        """Test Security of Budget Operating Unit"""
        # User 1 can list the budget assigned to
        # Main and B2C OU
        budget_ids =\
            self.BudgetObj.sudo(self.user1_id).\
            search([('operating_unit_id', 'in',
                     [self.ou1.id, self.b2c.id])]).ids
        self.assertNotEqual(budget_ids, [], 'User1 should have access to'
                            'Budget which belong to Main and B2C'
                            'Operating Unit.')
        # User 2 cannot list the budget assigned to Main OU
        budget_ids =\
            self.BudgetObj.sudo(self.user2_id).\
            search([('operating_unit_id', '=', self.ou1.id)]).ids
        self.assertEqual(budget_ids, [], 'User 2 should not be able to list'
                         'the budget assigned to Main Operating Unit.')
