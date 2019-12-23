# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestProject(common.TransactionCase):

    def setUp(self):
        super(TestProject, self).setUp()
        self.project_obj = self.env['project.project']
        self.task_obj = self.env['project.task']
        self.res_users_model = self.env['res.users']

        self.partner_1 = self.env['res.partner'].create({
            'name': 'SERPENTCS ',
            'email': 'serpentcs@gmail.com'})

        # Groups
        self.grp_mngr =\
            self.env.ref('project.group_project_manager')
        self.grp_user = self.env.ref('project.group_project_user')
        # Company
        self.company = self.env.ref('base.main_company')
        # Main Operating Unit
        self.main_OU = self.env.ref('operating_unit.main_operating_unit')
        # B2C Operating Unit
        self.b2c_OU = self.env.ref('operating_unit.b2c_operating_unit')
        # Create User 1 with Main OU
        self.user1 = self._create_user('user_1', [self.grp_mngr,
                                                  self.grp_user],
                                       self.company, [self.main_OU])
        # Create User 2 with B2C OU
        self.user2 = self._create_user('user_2', [self.grp_mngr,
                                                  self.grp_user],
                                       self.company, [self.b2c_OU])

        self.project1 = self._create_project(self.user1, self.main_OU)
        self.project2 = self._create_project(self.user2, self.b2c_OU)
        self.task1 = self._create_task(self.user1, self.project1)
        self.task2 = self._create_task(self.user2, self.project2)

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

    def _create_project(self, uid, operating_unit):
        project = self.project_obj.sudo(uid).create({
            'name': 'Test Project',
            'operating_unit_id': operating_unit.id,
            'privacy_visibility': 'employees',
            'partner_id': self.partner_1.id
        })
        return project

    def _create_task(self, uid, project):
        task = self.task_obj.create({
            'name': 'Test Task',
            'user_id': uid.id,
            'project_id': project.id
        })
        return task

    def test_project(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access Project for Main Operating Unit.
        projects = self.project_obj.sudo(self.user2.id).search(
            [('id', '=', self.project2.id),
             ('operating_unit_id', '=', self.main_OU.id)])
        self.assertEqual(projects.ids, [], 'User 2 should not have access to '
                         '%s' % self.main_OU.name)
        self.assertEqual(self.project1.operating_unit_id.id, self.main_OU.id)

    def test_project_task(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access Task for Main Operating Unit.
        tasks = self.task_obj.sudo(self.user2.id).search(
            [('id', '=', self.task2.id),
             ('operating_unit_id', '=', self.main_OU.id)])
        self.assertEqual(tasks.ids, [], 'User 2 should not have access to '
                         '%s' % self.main_OU.name)
        self.assertEqual(self.task1.operating_unit_id.id,
                         self.project1.operating_unit_id.id)
