# Copyright (C) 2026 CIT-Services <https://cit-services.eu/>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from unittest.mock import MagicMock, patch

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("-at_install", "post_install")
class TestIrHttp(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.operating_unit_1 = cls.env["operating.unit"].create(
            {
                "name": "Operating Unit 1",
                "code": "TEST_OU1",
                "partner_id": cls.env.company.partner_id.id,
            }
        )
        cls.operating_unit_2 = cls.env["operating.unit"].create(
            {
                "name": "Operating Unit 2",
                "code": "TEST_OU2",
                "partner_id": cls.env.company.partner_id.id,
            }
        )

        cls.user = cls.env["res.users"].create(
            {
                "name": "Test User",
                "login": "test_ou_user",
                "groups_id": [(6, 0, [cls.env.ref("base.group_user").id])],
                "operating_unit_ids": [
                    (6, 0, [cls.operating_unit_1.id, cls.operating_unit_2.id])
                ],
                "default_operating_unit_id": cls.operating_unit_1.id,
            }
        )

        cls.portal_user = cls.env["res.users"].create(
            {
                "name": "Portal User",
                "login": "test_ou_portal",
                "groups_id": [(6, 0, [cls.env.ref("base.group_portal").id])],
            }
        )

    def test_session_info_internal_user(self):
        """Test session_info for internal user includes operating unit data."""
        mock_request = MagicMock()
        mock_request.env.user = self.user
        mock_request.session.uid = self.user.id

        with (
            patch(
                "odoo.addons.web_easy_switch_operating_unit.models.ir_http.request",
                mock_request,
            ),
            patch(
                "odoo.addons.web.models.ir_http.request",
                mock_request,
            ),
        ):
            info = self.env["ir.http"].with_user(self.user).session_info()
            self.assertIn("user_operating_units", info)
            ou_data = info["user_operating_units"]
            self.assertEqual(
                ou_data["current_operating_unit"],
                (self.operating_unit_1.id, self.operating_unit_1.code),
            )

            allowed_ous = ou_data["allowed_operating_units"]
            self.assertEqual(len(allowed_ous), 2)
            self.assertIn(
                (self.operating_unit_1.id, self.operating_unit_1.code), allowed_ous
            )
            self.assertIn(
                (self.operating_unit_2.id, self.operating_unit_2.code), allowed_ous
            )

    def test_session_info_portal_user(self):
        """Test session_info for portal user does not include operating unit data."""
        mock_request = MagicMock()
        mock_request.env.user = self.portal_user
        mock_request.session.uid = self.portal_user.id

        with (
            patch(
                "odoo.addons.web_easy_switch_operating_unit.models.ir_http.request",
                mock_request,
            ),
            patch(
                "odoo.addons.web.models.ir_http.request",
                mock_request,
            ),
        ):
            info = self.env["ir.http"].with_user(self.portal_user).session_info()
            self.assertNotIn("user_operating_units", info)
