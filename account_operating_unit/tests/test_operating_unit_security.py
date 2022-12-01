# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import odoo.tests

from . import test_account_operating_unit as test_ou


@odoo.tests.tagged("post_install", "-at_install")
class TestOuSecurity(test_ou.TestAccountOperatingUnit):
    def test_security(self):
        """Test Security of Account Operating Unit"""
        # User 2 is only assigned to Operating Unit B2C, and cannot list
        # Journal Entries from Operating Unit B2B.
        move_ids = self.aml_model.with_user(self.user2_id.id).search(
            [("operating_unit_id", "=", self.b2b.id)]
        )
        self.assertFalse(
            move_ids, "user_2 should not have access to OU %s" % self.b2b.name
        )
