# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2019 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.fields import Command, Domain

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestResPartnerOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.res_partner_model = cls.env["res.partner"]
        cls.res_users_model = cls.env["res.users"]
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

    def test_search_partner_with_operating_unit(self):
        partners = self.res_partner_model.with_user(self.user1).search(
            Domain("name", "!=", "")
        )
        self.assertIn(self.partner1, partners)
        self.assertNotIn(self.partner2, partners)

    def test_search_count_partner_with_operating_unit(self):
        count = self.res_partner_model.with_user(self.user2).search_count(
            Domain("name", "!=", "")
        )
        self.assertGreaterEqual(count, 1)

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

        self.assertIn(self.b2c, user.partner_id.operating_unit_ids)
