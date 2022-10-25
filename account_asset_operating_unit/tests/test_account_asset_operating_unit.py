# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import time

from odoo.tests import common


class TestAccountAssetOperatingUnit(common.TransactionCase):
    def setUp(self):
        super(TestAccountAssetOperatingUnit, self).setUp()
        self.AccountAccount = self.env["account.account"]
        self.AccountAsset = self.env["account.asset"]
        self.ResUsers = self.env["res.users"]
        self.product_id = self.env["product.template"].search(
            [("type", "=", "service")], limit=1
        )
        # Groups
        self.grp_account_manager = self.env.ref("account.group_account_manager")
        self.group_user = self.env.ref("base.group_user")
        # Company
        self.company = self.env.ref("base.main_company")
        # Main Operating Unit
        self.main_OU = self.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        self.b2c_OU = self.env.ref("operating_unit.b2c_operating_unit")
        # Create User 1 with Main OU
        self.user1 = self._create_user(
            "user_1",
            [self.grp_account_manager, self.group_user],
            self.company,
            [self.main_OU],
        )
        # Create User 2 with B2C OU
        self.user2 = self._create_user(
            "user_2",
            [self.grp_account_manager, self.group_user],
            self.company,
            [self.b2c_OU],
        )
        # Accounts
        self.account_expense = self.AccountAccount.search(
            [
                ("company_id", "=", self.company.id),
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_expenses").id,
                ),
            ],
            limit=1,
        )
        self.account_asset = self.env["account.account"].search(
            [
                ("company_id", "=", self.company.id),
                (
                    "user_type_id",
                    "=",
                    self.env.ref("account.data_account_type_current_assets").id,
                ),
            ],
            limit=1,
        )
        # Journal
        self.journal_purchase = self.env["account.journal"].search(
            [("company_id", "=", self.company.id), ("type", "=", "purchase")], limit=1
        )
        # Asset Profile
        self.profile_id = self.env["account.asset.profile"].create(
            {
                "account_expense_depreciation_id": self.account_expense.id,
                "account_asset_id": self.account_asset.id,
                "account_depreciation_id": self.account_asset.id,
                "journal_id": self.journal_purchase.id,
                "name": "Hardware - 3 Years",
                "method_time": "year",
                "method_number": 3,
                "method_period": "year",
            }
        )
        self.asset1 = self._create_asset(self.user1.id, self.main_OU)
        self.asset2 = self._create_asset(self.user2.id, self.b2c_OU)

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.ResUsers.create(
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

    def _create_asset(self, uid, operating_unit):
        asset = self.AccountAsset.with_user(uid).create(
            {
                "name": "Test Asset",
                "profile_id": self.profile_id.id,
                "purchase_value": 1000,
                "salvage_value": 0,
                "date_start": time.strftime("%Y-01-01"),
                "method_time": "year",
                "method_number": 3,
                "method_period": "month",
                "operating_unit_id": operating_unit.id,
            }
        )
        return asset

    def test_asset(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access asset for Main Operating Unit.
        asset_ids = self.AccountAsset.with_user(self.user2.id).search(
            [
                ("id", "=", self.asset2.id),
                ("operating_unit_id", "=", self.main_OU.id),
            ]
        )
        self.assertEqual(
            asset_ids.ids,
            [],
            "User 2 should not have access to %s" % self.main_OU.name,
        )
        self.assertEqual(self.asset1.operating_unit_id.id, self.main_OU.id)
