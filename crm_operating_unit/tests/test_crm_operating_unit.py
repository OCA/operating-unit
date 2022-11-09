# © 2015-19 ForgeFlow S.L. - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.tests import common


class TestCrmOperatingUnit(common.TransactionCase):
    def setUp(self):
        super(TestCrmOperatingUnit, self).setUp()
        self.res_users_model = self.env["res.users"]
        self.crm_lead_model = self.env["crm.lead"]
        self.crm_team_model = self.env["crm.team"]
        # Groups
        self.grp_sale_mngr = self.env.ref("sales_team.group_sale_manager")
        self.grp_user = self.env.ref("base.group_user")
        # Company
        self.company = self.env.ref("base.main_company")
        # Main Operating Unit
        self.main_OU = self.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        self.b2c_OU = self.env.ref("operating_unit.b2c_operating_unit")
        # Create User 1 with Main OU
        self.user1 = self._create_user(
            "user_1", [self.grp_sale_mngr, self.grp_user], self.company, [self.main_OU]
        )
        # Create User 2 with B2C OU
        self.user2 = self._create_user(
            "user_2", [self.grp_sale_mngr, self.grp_user], self.company, [self.b2c_OU]
        )

        self.team1 = self._create_crm_team(self.user1.id, self.main_OU)
        self.team2 = self._create_crm_team(self.user2.id, self.b2c_OU)

        # Create CRM Leads
        self.lead1 = self._create_crm_lead(self.user1.id, self.team1)
        self.lead2 = self._create_crm_lead(self.user2.id, self.team2)

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
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

    def _create_crm_team(self, uid, operating_unit):
        """Create a sale order."""
        crm = self.crm_team_model.with_context(
            {"mail_create_nosubscribe": True, "mail_create_nolog": True}
        ).create(
            {"name": "CRM team", "operating_unit_id": operating_unit.id, "user_id": uid}
        )
        return crm

    def _create_crm_lead(self, uid, team):
        """Create a sale order."""
        operating_unit_id = self.crm_lead_model.with_user(
            uid
        )._get_default_operating_unit()
        crm = self.crm_lead_model.create(
            {
                "name": "CRM LEAD",
                "user_id": uid,
                "operating_unit_id": operating_unit_id.id,
                "team_id": team.id,
            }
        )
        return crm

    def test_crm_lead(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access CRM leads for Main Operating Unit.

        lead = self.crm_lead_model.with_user(self.user2.id).search(
            [("id", "=", self.lead1.id), ("operating_unit_id", "=", self.main_OU.id)]
        )
        self.assertEqual(
            lead.ids, [], "User 2 should not have access to " "%s" % self.main_OU.name
        )

    def test_team_ou(self):
        new_lead = self._create_crm_lead(self.user2.id, self.team2)
        self.assertEqual(
            new_lead.operating_unit_id,
            self.b2c_OU,
            "User 2 lead should have %s as operating unit" % self.b2c_OU.name,
        )
