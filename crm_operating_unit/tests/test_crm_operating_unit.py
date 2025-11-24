# © 2015-19 ForgeFlow S.L. - Jordi Ballester Alomar
# © 2015-17 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.fields import Command, Domain

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestCrmOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.crm_lead_model = cls.env["crm.lead"]
        cls.crm_team_model = cls.env["crm.team"]
        # Groups
        cls.grp_sale_mngr = cls.env.ref("sales_team.group_sale_manager")
        cls.grp_user = cls.env.ref("base.group_user")
        # Define User groups
        cls.user1.group_ids = [Command.set([cls.grp_sale_mngr.id, cls.grp_user.id])]
        cls.user2.group_ids = [Command.set([cls.grp_sale_mngr.id, cls.grp_user.id])]
        cls.team1 = cls._create_crm_team(cls.user1.id, cls.ou1)
        cls.team2 = cls._create_crm_team(cls.user2.id, cls.b2c)
        # Create CRM Leads
        cls.lead1 = cls._create_crm_lead(cls.user1.id, cls.team1)
        cls.lead2 = cls._create_crm_lead(cls.user2.id, cls.team2)

    @classmethod
    def _create_user(cls, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = cls.res_users_model.create(
            {
                "name": login,
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
        """Create a CRM team."""
        crm = cls.crm_team_model.with_context(
            mail_create_nosubscribe=True, mail_create_nolog=True
        ).create(
            {
                "name": "CRM team",
                "operating_unit_id": operating_unit.id,
                "user_id": uid,
                "company_id": operating_unit.company_id.id,
            }
        )
        return crm

    @classmethod
    def _create_crm_lead(cls, uid, team):
        """Create a CRM lead."""
        # Get the default operating unit for the user
        user = cls.env["res.users"].browse(uid)
        default_ou = (
            user.operating_unit_ids[0]
            if user.operating_unit_ids
            else team.operating_unit_id
        )
        crm = cls.crm_lead_model.create(
            {
                "name": "CRM LEAD",
                "user_id": uid,
                "operating_unit_id": default_ou.id,
                "team_id": team.id,
            }
        )
        return crm

    def test_crm_lead(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access CRM leads for Main Operating Unit.

        lead = self.crm_lead_model.with_user(self.user2.id).search(
            Domain.AND(
                [
                    Domain("id", "=", self.lead1.id),
                    Domain("operating_unit_id", "=", self.ou1.id),
                ]
            )
        )
        self.assertEqual(
            lead.ids,
            [],
            f"User 2 should not have access to {self.ou1.name}",
        )

    def test_team_ou(self):
        new_lead = self._create_crm_lead(self.user2.id, self.team2)
        self.assertEqual(
            new_lead.operating_unit_id,
            self.b2c,
            f"User 2 lead should have {self.b2c.name} as operating unit",
        )
