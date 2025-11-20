# Copyright 2016-17 ForgeFlow S.L. (http://www.forgeflow.com)
# Copyright 2017-TODAY Serpent Consulting Services Pvt. Ltd.
#   (<http://www.serpentcs.com>)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.fields import Command, Domain

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestSaleTeamOperatingUnit(OperatingUnitCommon):
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
        # Define User groups
        cls.user1.group_ids = [Command.set([cls.grp_sale_mngr.id, cls.grp_user.id])]
        cls.user2.group_ids = [Command.set([cls.grp_sale_mngr.id, cls.grp_user.id])]
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
                "company_ids": [Command.link(company.id)],
                "operating_unit_ids": [Command.link(ou.id) for ou in operating_units],
                "group_ids": [Command.set(group_ids)],
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
            Domain.AND(
                [
                    Domain("id", "=", self.team1.id),
                    Domain("operating_unit_id", "=", self.ou1.id),
                ]
            )
        )
        self.assertEqual(
            team.ids, [], f"User 2 should not have access to {self.ou1.name}"
        )
