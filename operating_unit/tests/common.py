# © 2017-TODAY ForgeFlow S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.models import Command
from odoo.tests import common


class OperatingUnitCommon(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.res_users_model = cls.env["res.users"].with_context(
            tracking_disable=True, no_reset_password=True
        )
        # Groups
        cls.grp_ou_mngr = cls.env.ref("operating_unit.group_manager_operating_unit")
        cls.grp_ou_multi = cls.env.ref("operating_unit.group_multi_operating_unit")
        # Company
        cls.company = cls.env.ref("base.main_company")
        cls.company_2 = cls.env["res.company"].create({"name": "Second company"})
        # Main Operating Unit
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        # B2C Operating Unit
        cls.b2c = cls.env.ref("operating_unit.b2c_operating_unit")
        # B2B Operating Unit
        cls.b2b = cls.env.ref("operating_unit.b2b_operating_unit")
        # Create User 1 with Main OU
        cls.user1 = cls._create_user("user_1", cls.grp_ou_mngr, cls.company, cls.ou1)
        # Create User 2 with B2C OU
        cls.user2 = cls._create_user("user_2", cls.grp_ou_multi, cls.company, cls.b2c)
        # Partner
        cls.partner1 = cls.env.ref("base.res_partner_1")

    @classmethod
    def _create_user(cls, login, group, company, operating_units, context=None):
        """Create a user."""
        user = cls.res_users_model.create(
            {
                "name": "Test User",
                "login": login,
                "password": "demo",
                "email": "test@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [Command.link(group.id)],
            }
        )
        return user

    def _create_operating_unit(self, uid, name, code, company_id=None):
        """Create Operating Unit"""
        if company_id is None:
            company_id = self.company
        ou = (
            self.env["operating.unit"]
            .with_user(uid)
            .create(
                {
                    "name": name,
                    "code": code,
                    "partner_id": company_id.partner_id.id,
                    "company_id": company_id.id,
                }
            )
        )
        return ou
