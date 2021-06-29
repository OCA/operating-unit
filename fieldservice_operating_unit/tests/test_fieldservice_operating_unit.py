# Copyright (C) 2021 Open Source Integrators
# Copyright (C) 2021 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from datetime import timedelta

from odoo import fields
from odoo.tests import common


class TestFSMOrder(common.TransactionCase):
    def setUp(self):
        super(TestFSMOrder, self).setUp()
        self.fsm_order_obj = self.env["fsm.order"]
        self.res_users_model = self.env["res.users"]
        self.test_location = self.env.ref("fieldservice.test_location")

        # Groups
        self.grp_fieldservice_mngr = self.env.ref("fieldservice.group_fsm_manager")
        self.grp_user = self.env.ref("base.group_user")
        # Company
        self.company = self.env.ref("base.main_company")
        # Main Operating Unit
        self.main_OU = self.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        self.b2c_OU = self.env.ref("operating_unit.b2c_operating_unit")
        # Create User 1 with Main OU
        self.user1 = self._create_user(
            "user_1",
            [self.grp_fieldservice_mngr, self.grp_user],
            self.company,
            [self.main_OU],
        )
        # Create User 2 with B2C OU
        self.user2 = self._create_user(
            "user_2",
            [self.grp_fieldservice_mngr, self.grp_user],
            self.company,
            [self.b2c_OU],
        )

        self.fsm_order1 = self._create_fsm_order(self.user1, self.main_OU)
        self.fsm_order2 = self._create_fsm_order(self.user2, self.b2c_OU)

    def _create_user(self, login, groups, company, operating_units):
        """ Create a user. """
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create(
            {
                "name": login,
                "login": login,
                "password": "demo",
                "email": "test@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user

    def _create_fsm_order(self, uid, operating_unit):
        fsm_order = self.fsm_order_obj.with_user(uid).create(
            {
                "location_id": self.test_location.id,
                "operating_unit_id": operating_unit.id,
                "date_start": fields.Datetime.today(),
                "date_end": fields.Datetime.today() + timedelta(hours=100),
                "request_early": fields.Datetime.today(),
            }
        )
        return fsm_order

    def test_fsm_order(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access FSM Orders for Main Operating Unit.
        fsm_orders = self.fsm_order_obj.with_user(self.user2).search(
            [
                ("id", "=", self.fsm_order2.id),
                ("operating_unit_id", "=", self.main_OU.id),
            ]
        )
        self.assertEqual(
            fsm_orders.ids,
            [],
            "User 2 should not have access to " "%s" % self.main_OU.name,
        )

        self.assertEqual(self.fsm_order1.operating_unit_id.id, self.main_OU.id)
