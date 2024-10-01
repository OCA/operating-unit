# Copyright 2024-TODAY Jérémy Didderen
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import json
from uuid import uuid4

from odoo import Command
from odoo.tests import HttpCase, common

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestSessionInfoOperatingUnit(OperatingUnitCommon, HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.allowed_ous = cls.ou1 + cls.b2b + cls.b2c

        cls.user_password = "info"
        cls.user = common.new_test_user(
            cls.env,
            "session",
            email="session@in.fo",
            password=cls.user_password,
            tz="UTC",
        )
        cls.user.write(
            {
                "default_operating_unit_id": cls.ou1.id,
                "operating_unit_ids": [Command.set(cls.allowed_ous.ids)],
            }
        )

        cls.payload = json.dumps(dict(jsonrpc="2.0", method="call", id=str(uuid4())))
        cls.headers = {
            "Content-Type": "application/json",
        }

    def test_session_info(self):
        self.authenticate(self.user.login, self.user_password)
        response = self.url_open(
            "/web/session/get_session_info", data=self.payload, headers=self.headers
        )
        self.assertEqual(response.status_code, 200)

        data = response.json()
        result = data["result"]

        expected_allowed_ous = {
            str(ou.id): {
                "id": ou.id,
                "name": ou.name,
                "sequence": ou.sequence,
            }
            for ou in self.allowed_ous
        }

        expected_user_companies = {
            "current_ou": self.ou1.id,
            "allowed_ous": expected_allowed_ous,
        }
        self.assertEqual(
            result["user_ous"],
            expected_user_companies,
            "The session_info['user_ous'] does not have the expected structure",
        )
