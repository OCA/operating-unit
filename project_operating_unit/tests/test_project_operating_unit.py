# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields
from odoo.tests import common


class TestProject(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.project_obj = cls.env["project.project"]
        cls.task_obj = cls.env["project.task"]
        cls.res_users_model = cls.env["res.users"]

        cls.partner_1 = cls.env["res.partner"].create(
            {"name": "SERPENTCS ", "email": "serpentcs@gmail.com"}
        )

        # Groups
        cls.grp_mngr = cls.env.ref("project.group_project_manager")
        cls.grp_user = cls.env.ref("project.group_project_user")
        # Company
        cls.company = cls.env.ref("base.main_company")
        # Main Operating Unit
        cls.main_OU = cls.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        cls.b2c_OU = cls.env.ref("operating_unit.b2c_operating_unit")
        # Create User 1 with Main OU
        cls.user1 = cls._create_user(
            "user_1", [cls.grp_mngr, cls.grp_user], cls.company, [cls.main_OU]
        )
        # Create User 2 with B2C OU
        cls.user2 = cls._create_user(
            "user_2", [cls.grp_mngr, cls.grp_user], cls.company, [cls.b2c_OU]
        )

        cls.project1 = cls._create_project(cls.user1, cls.main_OU)
        cls.project2 = cls._create_project(cls.user2, cls.b2c_OU)
        cls.task1 = cls._create_task(cls.user1, cls.project1)
        cls.task2 = cls._create_task(cls.user2, cls.project2)

    @classmethod
    def _create_user(cls, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = cls.res_users_model.create(
            {
                "name": login,
                "login": login,
                "password": "demo",
                "email": "test@yourcompany.com",
                "company_id": company.id,
                "company_ids": [fields.Command.link(company.id)],
                "operating_unit_ids": [
                    fields.Command.link(ou.id) for ou in operating_units
                ],
                "groups_id": [fields.Command.set(group_ids)],
            }
        )
        return user

    @classmethod
    def _create_project(cls, uid, operating_unit):
        project = cls.project_obj.with_user(uid).create(
            {
                "name": "Test Project",
                "operating_unit_id": operating_unit.id,
                "privacy_visibility": "employees",
                "partner_id": cls.partner_1.id,
            }
        )
        return project

    @classmethod
    def _create_task(cls, uid, project):
        task = cls.task_obj.create(
            {
                "name": "Test Task",
                "user_ids": [fields.Command.link(uid.id)],
                "project_id": project.id,
            }
        )
        return task

    def test_project(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access Project for Main Operating Unit.
        projects = self.project_obj.with_user(self.user2.id).search(
            [("id", "=", self.project2.id), ("operating_unit_id", "=", self.main_OU.id)]
        )
        self.assertEqual(
            projects.ids,
            [],
            "User 2 should not have access to " "%s" % self.main_OU.name,
        )
        self.assertEqual(self.project1.operating_unit_id.id, self.main_OU.id)

    def test_project_task(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access Task for Main Operating Unit.
        tasks = self.task_obj.with_user(self.user2.id).search(
            [("id", "=", self.task2.id), ("operating_unit_id", "=", self.main_OU.id)]
        )
        self.assertEqual(
            tasks.ids, [], "User 2 should not have access to " "%s" % self.main_OU.name
        )
        self.assertEqual(
            self.task1.operating_unit_id.id, self.project1.operating_unit_id.id
        )
