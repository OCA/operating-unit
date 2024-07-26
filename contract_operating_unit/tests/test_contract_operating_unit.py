# Copyright 2020 ForgeFlow S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo.addons.contract.tests.test_contract import TestContractBase


class TestContractOperatingUnit(TestContractBase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.res_users_model = cls.env["res.users"]

        cls.company = cls.env.ref("base.main_company")
        cls.grp_contract_manager = cls.env.ref("account.group_account_manager")
        cls.contract_model = cls.env["contract.contract"]
        cls.group_user = cls.env.ref("base.group_user")

        # Main Operating Unit
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        cls.b2c = cls.env.ref("operating_unit.b2c_operating_unit")

        # Create Users
        cls.user1 = cls._create_user(
            "User_1",
            [cls.grp_contract_manager, cls.group_user],
            cls.company,
            [cls.ou1, cls.b2c],
        )
        cls.user2 = cls._create_user(
            "User_2",
            [cls.grp_contract_manager, cls.group_user],
            cls.company,
            [cls.b2c],
        )
        cls.contract.operating_unit_id = cls.ou1
        cls.contract2.operating_unit_id = cls.b2c

    @classmethod
    def _create_user(cls, login, groups, company, operating_units, context=None):
        """Creates a user."""
        group_ids = [group.id for group in groups]
        user = cls.res_users_model.create(
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
                ("id", "=", self.contract.id),
                ("operating_unit_id", "=", self.ou1.id),
            ]
        )
        self.assertFalse(
            record,
            "User 2 should not have access to OU %s" % self.ou1.name,
        )

    def test_default(self):
        """Test that the user's OU is used when creating a contract"""
        contract = (
            self.env["contract.contract"]
            .with_user(self.user1)
            .create(
                {
                    "name": "A contract",
                    "partner_id": self.env["res.partner"]
                    .search([], order="customer_rank desc", limit=1)
                    .id,
                }
            )
        )
        self.assertEqual(contract.operating_unit_id, self.ou1)

    def test_contract_invoice(self):
        """Test that invoices from contracts get the contract's OU assigned"""
        invoice = self.contract2._recurring_create_invoice()
        self.assertEqual(invoice.operating_unit_id, self.b2c)
