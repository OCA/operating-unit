# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.exceptions import UserError
from odoo.fields import Command, Domain

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestResPartnerOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.res_partner_model = cls.env["res.partner"]
        cls.grp_user = cls.env.ref("base.group_user")
        # Define User groups
        cls.user1.group_ids = [Command.set([cls.grp_user.id])]
        cls.user2.group_ids = [Command.set([cls.grp_user.id])]
        # Create Partner 1 with Main OU
        cls.partner1 = cls._create_partner("Test Partner 1", cls.ou1)
        # Create Partner 2 with B2C OU
        cls.partner2 = cls._create_partner("Test Partner 2", cls.b2c)

    @classmethod
    def _create_partner(cls, name, operating_unit, context=None):
        """Create a partner."""
        partner = cls.res_partner_model.create(
            {
                "name": name,
                "operating_unit_ids": [Command.link(operating_unit.id)],
            }
        )
        return partner

    def test_create_user_adds_ou_to_partner(self):
        new_user = self._create_user(
            "new_user_ou", self.grp_ou_mngr, self.company, [self.ou1]
        )
        self.assertIn(self.ou1, new_user.partner_id.operating_unit_ids)

    def test_write_user_adds_new_ou_to_partner(self):
        new_user = self._create_user(
            "edit_user_ou", self.grp_ou_mngr, self.company, [self.ou1]
        )
        self.assertIn(self.ou1, new_user.partner_id.operating_unit_ids)

        new_user.write(
            {
                "default_operating_unit_id": self.b2c.id,
                "operating_unit_ids": [Command.link(self.b2c.id)],
            }
        )

        self.assertIn(self.b2c, new_user.partner_id.operating_unit_ids)
        self.assertIn(self.ou1, new_user.partner_id.operating_unit_ids)

    def test_write_user_removes_ou_from_partner(self):
        """Removing an OU from the user also removes it from the partner."""
        new_user = self._create_user(
            "remove_user_ou", self.grp_ou_mngr, self.company, [self.ou1, self.b2c]
        )
        new_user.default_operating_unit_id = self.ou1
        self.assertIn(self.ou1, new_user.partner_id.operating_unit_ids)
        self.assertIn(self.b2c, new_user.partner_id.operating_unit_ids)

        new_user.write(
            {
                "operating_unit_ids": [Command.unlink(self.b2c.id)],
            }
        )

        self.assertIn(self.ou1, new_user.partner_id.operating_unit_ids)
        self.assertNotIn(self.b2c, new_user.partner_id.operating_unit_ids)

    def test_write_partner_incompatible_ou_raises_error(self):
        """Directly setting partner OUs to a set that differs from the user's raises
        UserError."""
        user = self._create_user(
            "partner_ou_guard", self.grp_ou_mngr, self.company, [self.ou1, self.b2c]
        )
        user.default_operating_unit_id = self.ou1
        self.assertEqual(
            user.partner_id.operating_unit_ids, user.assigned_operating_unit_ids
        )

        with self.assertRaises(UserError):
            # Set only ou1 on the partner — diverges from user's [ou1, b2c]
            user.partner_id.write({"operating_unit_ids": [Command.set([self.ou1.id])]})

    def test_write_partner_compatible_ou_no_error(self):
        """Setting partner OUs to exactly match the linked user's OUs must NOT raise."""
        user = self._create_user(
            "partner_ou_compat", self.grp_ou_mngr, self.company, [self.ou1]
        )
        # Should succeed without error
        user.partner_id.write({"operating_unit_ids": [Command.set([self.ou1.id])]})
        self.assertEqual(
            user.partner_id.operating_unit_ids, user.assigned_operating_unit_ids
        )

    def test_search_partner_with_operating_unit(self):
        """search() filters partners by the calling user's OUs."""
        partners = self.res_partner_model.with_user(self.user1).search(
            Domain("name", "!=", "")
        )
        self.assertIn(self.partner1, partners)
        self.assertNotIn(self.partner2, partners)

    def test_search_includes_partner_without_ou(self):
        """Partners with no OUs must be visible to every user."""
        partner_no_ou = self.res_partner_model.create({"name": "No OU Partner"})
        self.assertFalse(partner_no_ou.operating_unit_ids)

        partners_user1 = self.res_partner_model.with_user(self.user1).search(
            Domain("name", "=", "No OU Partner")
        )
        partners_user2 = self.res_partner_model.with_user(self.user2).search(
            Domain("name", "=", "No OU Partner")
        )
        self.assertIn(partner_no_ou, partners_user1)
        self.assertIn(partner_no_ou, partners_user2)

    def test_search_count_partner_with_operating_unit(self):
        """search_count() respects the calling user's OUs."""
        count = self.res_partner_model.with_user(self.user2).search_count(
            Domain("name", "!=", "")
        )
        self.assertGreaterEqual(count, 1)
        count_user1 = self.res_partner_model.with_user(self.user1).search_count(
            Domain("name", "in", [self.partner1.name, self.partner2.name])
        )
        # user1 has ou1 → sees partner1 (ou1), not partner2 (b2c)
        self.assertEqual(count_user1, 1)
        count_user2 = self.res_partner_model.with_user(self.user2).search_count(
            Domain("name", "in", [self.partner1.name, self.partner2.name])
        )
        # user2 has b2c → sees partner2 (b2c), not partner1 (ou1)
        self.assertEqual(count_user2, 1)

    def test_create_user_partner_already_has_ou_syncs_to_user(self):
        """Creating a user whose partner already has different OUs syncs the
        partner's OUs to the user's OUs."""
        partner = self.res_partner_model.create(
            {
                "name": "Pre-existing OU Partner",
                "operating_unit_ids": [Command.set([self.ou1.id])],
            }
        )
        new_user = self.res_users_model.create(
            {
                "name": "User Linked Partner",
                "login": "user_linked_partner",
                "password": "demo",
                "email": "linked@test.com",
                "company_id": self.company.id,
                "company_ids": [Command.link(self.company.id)],
                "operating_unit_ids": [Command.link(self.b2c.id)],
                "partner_id": partner.id,
            }
        )
        self.assertEqual(
            new_user.partner_id.operating_unit_ids, new_user.assigned_operating_unit_ids
        )
        self.assertIn(self.b2c, new_user.partner_id.operating_unit_ids)
        self.assertNotIn(self.ou1, new_user.partner_id.operating_unit_ids)

    def test_create_user_partner_already_has_matching_ou_no_error(self):
        """Creating a user whose partner already has exactly the same OUs
        must NOT raise."""
        partner = self.res_partner_model.create(
            {
                "name": "Matching OU Partner",
                "operating_unit_ids": [Command.set([self.ou1.id])],
            }
        )
        new_user = self.res_users_model.create(
            {
                "name": "User Matching Partner",
                "login": "user_matching_partner",
                "password": "demo",
                "email": "matching@test.com",
                "company_id": self.company.id,
                "company_ids": [Command.link(self.company.id)],
                "operating_unit_ids": [Command.link(self.ou1.id)],
                "default_operating_unit_id": self.ou1.id,
                "partner_id": partner.id,
            }
        )
        self.assertEqual(
            new_user.partner_id.operating_unit_ids, new_user.assigned_operating_unit_ids
        )

    def test_create_user_with_default_operating_unit(self):
        new_user = self.res_users_model.create(
            {
                "name": "Create With Default OU",
                "login": "user_with_default_ou",
                "password": "demo",
                "email": "user@default.com",
                "company_id": self.company.id,
                "company_ids": [Command.link(self.company.id)],
                "operating_unit_ids": [Command.link(self.ou1.id)],
                "default_operating_unit_id": self.ou1.id,
            }
        )

        self.assertIn(self.ou1, new_user.partner_id.operating_unit_ids)

    def test_write_user_sets_default_operating_unit(self):
        user = self._create_user(
            "write_user_default_ou", self.grp_ou_mngr, self.company, [self.ou1]
        )
        self.assertIn(self.ou1, user.partner_id.operating_unit_ids)

        user.write(
            {
                "default_operating_unit_id": self.b2c.id,
                "operating_unit_ids": [
                    Command.link(self.ou1.id),
                    Command.link(self.b2c.id),
                ],
            }
        )

        self.assertIn(self.ou1, user.partner_id.operating_unit_ids)
        self.assertIn(self.b2c, user.partner_id.operating_unit_ids)
