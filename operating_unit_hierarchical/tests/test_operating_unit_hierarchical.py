# Copyright 2020 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.addons.operating_unit.tests.test_operating_unit import (
    TestOperatingUnit as _TestOperatingUnit,
)


class TestOperatingUnitHierarchical(_TestOperatingUnit):
    def test_20_hierarchy(self):
        self.assertEqual(self.b2c.parent_level, 0)
        self.b2c_child = self._create_operating_unit(
            self.user1.id, "A B2C child", "B2C_C"
        )
        self.b2c_child.parent_id = self.b2c
        self.assertEqual(self.b2c_child.parent_level, 1)
        self.assertEqual(
            self.b2c_child.display_name,
            " / ".join([self.b2c.name, self.b2c_child.name]),
            "Display name shows hierarchy path",
        )
        user2_uos = self.env["operating.unit"].with_user(self.user2).search([])
        self.assertEqual(
            len(user2_uos), 2, "User2 should see child OUs of assigned OUs"
        )
        self.assertEqual(user2_uos.mapped("code"), ["B2C", "B2C_C"])
