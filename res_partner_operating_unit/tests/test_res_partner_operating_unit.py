# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2020 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import Command
from odoo.exceptions import UserError

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestResPartnerOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(
            context=dict(cls.env.context, tracking_disable=True, no_reset_password=True)
        )
        # Create Partner 1 with Main OU
        cls.partner1 = cls._create_partner("Test Partner 1", cls.ou1)
        # Create Partner 2 with B2C OU
        cls.partner2 = cls._create_partner("Test Partner 2", cls.b2c)

    @classmethod
    def _create_partner(cls, name, operating_units):
        """Create a partner."""
        partner = cls.env["res.partner"].create(
            {
                "name": name,
                "operating_unit_ids": [Command.link(ou.id) for ou in operating_units],
            }
        )
        return partner

    def test_01_partner_operating_unit(self):
        """Test Partner Operating Unit."""
        self.assertEqual(self.user1.default_operating_unit_id, self.ou1)
        self.assertEqual(self.user2.default_operating_unit_id, self.ou1)

        self.user1.operating_unit_ids = [Command.link(self.b2c.id)]
        self.user2.operating_unit_ids = [Command.link(self.ou1.id)]
        self.assertIn(self.b2c, self.user1.partner_id.operating_unit_ids)
        self.assertIn(self.ou1, self.user2.partner_id.operating_unit_ids)

        self.assertEqual(self.partner1.operating_unit_ids, self.ou1)
        self.assertEqual(self.partner2.operating_unit_ids, self.b2c)

    def test_write_user_removes_ou_from_partner(self):
        """Removing an OU from the user also removes it from the partner."""
        new_user = self._create_user(
            "remove_user_ou", self.grp_ou_mngr, self.company, [self.ou1, self.b2c]
        )
        self.assertIn(self.ou1, new_user.partner_id.operating_unit_ids)
        self.assertIn(self.b2c, new_user.partner_id.operating_unit_ids)

        new_user.write({"operating_unit_ids": [Command.unlink(self.b2c.id)]})

        self.assertIn(self.ou1, new_user.partner_id.operating_unit_ids)
        self.assertNotIn(self.b2c, new_user.partner_id.operating_unit_ids)

    def test_write_partner_incompatible_ou_raises_error(self):
        """Directly setting partner OUs to a set that differs from the
        user's raises UserError."""
        user = self._create_user(
            "partner_ou_guard", self.grp_ou_mngr, self.company, [self.ou1, self.b2c]
        )
        self.assertEqual(
            user.partner_id.operating_unit_ids, user.assigned_operating_unit_ids
        )

        with self.assertRaises(UserError):
            # Set only ou1 on the partner — diverges from user's [ou1, b2c]
            user.partner_id.write({"operating_unit_ids": [Command.set([self.ou1.id])]})

    def test_write_partner_compatible_ou_no_error(self):
        """Setting partner OUs to exactly match the linked user's OUs must
        NOT raise."""
        user = self._create_user(
            "partner_ou_compat", self.grp_ou_mngr, self.company, [self.ou1]
        )
        # Should succeed without error
        user.partner_id.write({"operating_unit_ids": [Command.set([self.ou1.id])]})
        self.assertEqual(
            user.partner_id.operating_unit_ids, user.assigned_operating_unit_ids
        )

    def test_create_user_partner_already_has_ou_syncs_to_user(self):
        """Creating a user whose partner already has different OUs syncs the
        partner's OUs to the user's OUs."""
        partner = self.env["res.partner"].create(
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
        partner = self.env["res.partner"].create(
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
