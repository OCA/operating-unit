# -*- coding: utf-8 -*-
# Copyright 2016-17 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# Copyright 2016-17 Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import common


class TestHrContractOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestHrContractOperatingUnit, self).setUp()

        self.res_users_model = self.env['res.users']
        self.hr_contract_model = self.env['hr.contract']
        self.hr_employee_model = self.env['hr.employee']

        self.company = self.env.ref('base.main_company')
        self.contract_type = self.env.ref('hr_contract.hr_contract_type_emp')
        self.grp_hr_manager = self.env.ref('hr.group_hr_manager')

        # Main Operating Unit
        self.ou1 = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c = self.env.ref('operating_unit.b2c_operating_unit')

        # Create Users
        self.user1 = self._create_user('User_1', self.grp_hr_manager,
                                       self.company, [self.ou1, self.b2c])
        self.user2 = self._create_user('User_2', self.grp_hr_manager,
                                       self.company, [self.b2c])

        # Create Employee
        self.emp = self._create_hr_employee()

        # Create Contracts
        self.hr_contract1 = self._create_hr_contract(self.user1, self.ou1)
        self.hr_contract2 = self._create_hr_contract(self.user2, self.b2c)

    def _create_user(self, login, groups, company, operating_units,
                     context=None):
        """Creates a user."""
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create({
            'name': 'Test HR Contract User',
            'login': login,
            'password': 'demo',
            'email': 'example@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'groups_id': [(6, 0, group_ids)]
        })
        return user

    def _create_hr_employee(self):
        """Creates an employee."""
        emp = self.hr_employee_model.create({
            'name': "Test Employee",
            })
        return emp

    def _create_hr_contract(self, uid, operating_unit):
        """Creates a contract for an employee."""
        contract = self.hr_contract_model.sudo(uid).create({
            'name': "Sample Contract",
            'operating_unit_id': operating_unit.id,
            'employee_id': self.emp.id,
            'type_id': self.contract_type.id,
            'wage': '10000',
            })
        return contract

    def test_hr_contract_ou(self):
        """Test Hr Contract Operating Unit"""
        # User 2 is only assigned to Operating Unit B2C, and cannot
        # Access Hr Contract records of Main Operating Unit.
        record = self.hr_contract_model.sudo(self.user2.id).search(
            [('id', '=', self.hr_contract1.id),
             ('operating_unit_id', '=', self.ou1.id)])
        self.assertEqual(record.ids, [], 'User 2 should not have access to '
                         'OU %s' % self.ou1.name)
