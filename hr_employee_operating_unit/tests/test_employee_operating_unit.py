# -*- coding: utf-8 -*-
# © 2017 Genweb2 Limited - Matiar Rahman
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common


class TestEmployeeOperatingUnit(common.TransactionCase):

    def setUp(self):
        super(TestEmployeeOperatingUnit, self).setUp()
        self.res_users_model = self.env['res.users']
        self.hr_employee_model = self.env['hr.employee']
        # Groups
        self.hr_officer = self.env.ref('hr.group_hr_user')
        self.grp_user = self.env.ref('base.group_user')
        # Company
        self.company = self.env.ref('base.main_company')
        # Main Operating Unit
        self.main_OU = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c_OU = self.env.ref('operating_unit.b2c_operating_unit')
        # Create User 1 with Main OU
        self.user1 = self._create_user('user_1', [self.hr_officer,
                                                  self.grp_user],
                                       self.company, [self.main_OU])
        # Create User 2 with B2C OU
        self.user2 = self._create_user('user_2', [self.hr_officer,
                                                  self.grp_user],
                                       self.company, [self.b2c_OU])

        # Create Employee
        self.emp1 = self._create_employee(self.user1.id)
        self.emp2 = self._create_employee(self.user2.id)

    def _create_user(self, login, groups, company, operating_units):
        """ Create a user. """
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create({
            'name': login,
            'login': login,
            'password': 'demo',
            'email': 'test@yourcompany.com',
            'company_id': company.id,
            'company_ids': [(4, company.id)],
            'operating_unit_ids': [(4, ou.id) for ou in operating_units],
            'groups_id': [(6, 0, group_ids)]
        })
        return user

    def _create_employee(self, uid):
        """Create an employee."""
        operating_unit_id = self.hr_employee_model.sudo(uid). \
            _get_operating_unit()
        employee = self.hr_employee_model.create({
            'name': 'Employee',
            'user_id': uid,
            'operating_unit_ids': [(4, operating_unit_id.id)]
        })
        return employee

    def test_employee(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access Employee for Main Operating Unit.

        emp = self.hr_employee_model.sudo(self.user2.id).search(
            [('id', '=', self.emp1.id),
             ('operating_unit_ids', '=', self.main_OU.id)])
        self.assertEqual(emp.ids, [], 'User 2 should not have access to '
                         '%s' % self.main_OU.name)
