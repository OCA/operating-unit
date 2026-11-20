# Copyright 2026 Jarsa (https://www.jarsa.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.fields import Command

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestOperatingUnitAccessAll(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.grp_all_ou = cls.env.ref(
            "operating_unit_access_all.group_all_operating_unit"
        )
        cls.all_ous = cls.env["operating.unit"].search([])

    def _visible_ous(self, user):
        return self.env["operating.unit"].with_user(user).search([])

    def test_user_without_group_sees_only_assigned(self):
        self.assertEqual(self._visible_ous(self.user2), self.b2c)

    def test_user_with_group_sees_all(self):
        self.user2.group_ids = [Command.link(self.grp_all_ou.id)]
        self.assertEqual(self._visible_ous(self.user2), self.all_ous)
        # The user can read an OU that is not assigned to them
        self.assertEqual(self.b2b.with_user(self.user2).name, "B2B")
        # Assigned operating units are not changed by the group
        self.assertEqual(self.user2.assigned_operating_unit_ids, self.b2c)

    def test_remove_group_restores_restriction(self):
        self.user2.group_ids = [Command.link(self.grp_all_ou.id)]
        self.assertEqual(self._visible_ous(self.user2), self.all_ous)
        self.user2.group_ids = [Command.unlink(self.grp_all_ou.id)]
        self.assertEqual(self._visible_ous(self.user2), self.b2c)

    def test_group_does_not_grant_write(self):
        self.user2.group_ids = [Command.link(self.grp_all_ou.id)]
        self.assertFalse(
            self.env["operating.unit"].with_user(self.user2).has_access("write")
        )

    def test_company_restriction_still_applies(self):
        ou_company_2 = self.env["operating.unit"].create(
            {
                "name": "Second company OU",
                "code": "SC2",
                "partner_id": self.partner.id,
                "company_id": self.company_2.id,
            }
        )
        self.user2.group_ids = [Command.link(self.grp_all_ou.id)]
        self.assertNotIn(ou_company_2, self._visible_ous(self.user2))
