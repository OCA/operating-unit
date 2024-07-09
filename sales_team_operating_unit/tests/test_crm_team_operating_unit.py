# Copyright 2016-17 ForgeFlow S.L. (http://www.forgeflow.com)
# Copyright 2017-TODAY Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common


class TestSaleTeamOperatingUnit(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.res_users_model = cls.env["res.users"].with_context(
            tracking_disable=True, no_reset_password=True
        )
        cls.crm_team_model = cls.env["crm.team"]
        # Groups
        cls.grp_sale_mngr = cls.env.ref("sales_team.group_sale_manager")
        cls.grp_user = cls.env.ref("operating_unit.group_multi_operating_unit")
        # Company
        cls.company = cls.env.ref("base.main_company")
        # Main Operating Unit
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        cls.b2c = cls.env.ref("operating_unit.b2c_operating_unit")
        # Create User 1 with Main OU

        cls.user1 = cls._create_user(
            "user_1", [cls.grp_sale_mngr, cls.grp_user], cls.company, [cls.ou1]
        )
        # Create User 2 with B2C OU
        cls.user2 = cls._create_user(
            "user_2", [cls.grp_sale_mngr, cls.grp_user], cls.company, [cls.b2c]
        )
        # Create CRM teams
        cls.team1 = cls._create_crm_team(cls.user1.id, cls.ou1)
        cls.team2 = cls._create_crm_team(cls.user2.id, cls.b2c)

    @classmethod
    def _create_user(cls, login, groups, company, operating_units, context=None):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = cls.res_users_model.create(
            {
                "name": "Test User",
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

    @classmethod
    def _create_crm_team(cls, uid, operating_unit):
        """Create a Sales Team."""
        crm = cls.crm_team_model.with_user(uid).create(
            {
                "name": "CRM team",
                "operating_unit_id": operating_unit.id,
                "company_id": cls.company.id,
            }
        )
        return crm

    def test_crm_team(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access CRM teams for Main Operating Unit.
        team = self.crm_team_model.with_user(self.user2.id).search(
            [("id", "=", self.team1.id), ("operating_unit_id", "=", self.ou1.id)]
        )
        self.assertEqual(
            team.ids, [], "User 2 should not have access to " "%s" % self.ou1.name
        )
