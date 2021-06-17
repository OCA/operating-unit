# Copyright 2020 ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import common


class TestContractOperatingUnit(common.TransactionCase):
    def setUp(self):
        super(TestContractOperatingUnit, self).setUp()

        self.res_users_model = self.env["res.users"]
        self.contract_model = self.env["contract.contract"]

        self.company = self.env.ref("base.main_company")
        self.grp_contract_manager = self.env.ref("account.group_account_manager")
        self.group_user = self.env.ref("base.group_user")

        # Main Operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        self.b2c = self.env.ref("operating_unit.b2c_operating_unit")

        # Create Users
        self.user1 = self._create_user(
            "User_1",
            [self.grp_contract_manager, self.group_user],
            self.company,
            [self.ou1, self.b2c],
        )
        self.user2 = self._create_user(
            "User_2",
            [self.grp_contract_manager, self.group_user],
            self.company,
            [self.b2c],
        )

        self.partner = self.env["res.partner"].create(
            {
                "name": "Test contract partner",
            }
        )

        self.contract1 = (
            self.env["contract.contract"]
            .with_user(self.user1.id)
            .create(
                {
                    "name": "Maintenance of Servers",
                    "partner_id": self.partner.id,
                    "operating_unit_id": self.ou1.id,
                }
            )
        )
        self.contract2 = (
            self.env["contract.contract"]
            .with_user(self.user2.id)
            .create(
                {
                    "name": "Maintenance of Servers",
                    "partner_id": self.partner.id,
                    "operating_unit_id": self.b2c.id,
                }
            )
        )

    def _create_user(self, login, groups, company, operating_units, context=None):
        """Creates a user."""
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create(
            {
                "name": "Test Contract User",
                "login": login,
                "password": "demo",
                "email": "example@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user

    def test_contract_ou(self):
        """Test Contract Operating Unit"""
        # User 2 is only assigned to Operating Unit B2C, and cannot
        # Access Contract records of Main Operating Unit.
        record = self.contract_model.with_user(self.user2.id).search(
            [
                ("id", "=", self.contract1.id),
                ("operating_unit_id", "=", self.ou1.id),
            ]
        )
        self.assertEqual(
            record.ids,
            [],
            "User 2 should not have access to " "OU %s" % self.ou1.name,
        )
