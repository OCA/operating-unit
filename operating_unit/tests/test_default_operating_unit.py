# Copyright 2026 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.exceptions import ValidationError
from odoo.fields import Command
from odoo.tests import Form, tagged

from .common import OperatingUnitCommon


@tagged("post_install", "-at_install")
class TestDefaultOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ou_c2_a = cls._create_company_ou("C2 Branch A", "C2A")
        cls.ou_c2_b = cls._create_company_ou("C2 Branch B", "C2B")

    @classmethod
    def _create_company_ou(cls, name, code):
        return cls.env["operating.unit"].create(
            {
                "name": name,
                "code": code,
                "partner_id": cls.company_2.partner_id.id,
                "company_id": cls.company_2.id,
            }
        )

    def test_01_new_users_get_company_default_operating_units(self):
        """An admin sets the OUs granted to new users of the second company:
        users created there get them, users of the main company keep getting
        the OU of the admin."""
        settings = Form(self.env["res.config.settings"].with_company(self.company_2))
        settings.new_user_operating_unit_ids.add(self.ou_c2_a)
        settings.new_user_operating_unit_ids.add(self.ou_c2_b)
        settings.new_user_default_operating_unit_id = self.ou_c2_b
        settings.save().execute()
        self.assertEqual(
            self.company_2.new_user_operating_unit_ids,
            self.ou_c2_a | self.ou_c2_b,
        )

        # created through the API with an explicit company
        user = self.res_users_model.create(
            {
                "name": "C2 User",
                "login": "c2_user",
                "company_id": self.company_2.id,
                "company_ids": [Command.link(self.company_2.id)],
            }
        )
        self.assertEqual(user.assigned_operating_unit_ids, self.ou_c2_a | self.ou_c2_b)
        self.assertEqual(user.default_operating_unit_id, self.ou_c2_b)

        # created from the form while working in the second company
        user_form = Form(self.env["res.users"].with_company(self.company_2))
        user_form.name = "C2 Form User"
        user_form.login = "c2_form_user"
        user = user_form.save()
        self.assertEqual(user.assigned_operating_unit_ids, self.ou_c2_a | self.ou_c2_b)
        self.assertEqual(user.default_operating_unit_id, self.ou_c2_b)

        # main company has no defaults: fallback to the creator's OU
        user = self.res_users_model.create(
            {"name": "Main User", "login": "main_user", "company_id": self.company.id}
        )
        self.assertEqual(
            user.default_operating_unit_id, self.env.user.default_operating_unit_id
        )
        self.assertEqual(
            user.assigned_operating_unit_ids, self.env.user.default_operating_unit_id
        )

        # explicit OUs are never overridden
        user = self.res_users_model.create(
            {
                "name": "Explicit User",
                "login": "explicit_user",
                "company_id": self.company_2.id,
                "company_ids": [Command.link(self.company_2.id)],
                "assigned_operating_unit_ids": [Command.set(self.ou_c2_a.ids)],
            }
        )
        self.assertEqual(user.assigned_operating_unit_ids, self.ou_c2_a)

    def test_02_operating_units_of_another_company_refused(self):
        """An admin cannot grant new users of the second company an OU of the
        main company, neither as allowed nor as default OU."""
        with self.assertRaisesRegex(ValidationError, "must belong to company"):
            self.company_2.new_user_operating_unit_ids = self.ou1
        with self.assertRaisesRegex(ValidationError, "must belong to company"):
            self.company_2.new_user_default_operating_unit_id = self.ou1

    def test_03_default_operating_unit_is_always_allowed(self):
        """An admin only sets the default OU of the second company: new users
        there are also allowed on it."""
        self.company_2.new_user_default_operating_unit_id = self.ou_c2_a
        user = self.res_users_model.create(
            {
                "name": "C2 User",
                "login": "c2_user",
                "company_id": self.company_2.id,
                "company_ids": [Command.link(self.company_2.id)],
            }
        )
        self.assertEqual(user.assigned_operating_unit_ids, self.ou_c2_a)
        self.assertEqual(user.default_operating_unit_id, self.ou_c2_a)
