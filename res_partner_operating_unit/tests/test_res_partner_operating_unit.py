# © 2017 Niaga Solution - Edi Santoso <repodevs@gmail.com>
# Copyright (C) 2020 Serpent Consulting Services
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import Command

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

        self.user1.default_operating_unit_id = self.b2c
        self.user2.default_operating_unit_id = self.ou1
        self.assertIn(self.b2c, self.user1.partner_id.operating_unit_ids)
        self.assertIn(self.ou1, self.user2.partner_id.operating_unit_ids)

        self.assertEqual(self.partner1.operating_unit_ids, self.ou1)
        self.assertEqual(self.partner2.operating_unit_ids, self.b2c)
