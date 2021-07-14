# Copyright (C) 2021 Open Source Integrators
# Copyright (C) 2021 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.tests import common


class TestAgreementOperatingUnit(common.TransactionCase):
    def setUp(self):
        super(TestAgreementOperatingUnit, self).setUp()
        self.agreement_obj = self.env["agreement"]
        self.serviceprofile_obj = self.env["agreement.serviceprofile"]
        self.res_users_model = self.env["res.users"]
        self.product_id = self.env["product.template"].search(
            [("type", "=", "service")], limit=1
        )

        # Groups
        self.grp_agreement_manager = self.env.ref(
            "agreement_legal.group_agreement_manager"
        )
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
            [self.grp_agreement_manager, self.group_user],
            self.company,
            [self.main_OU],
        )
        # Create User 2 with B2C OU
        self.user2 = self._create_user(
            "user_2",
            [self.grp_agreement_manager, self.group_user],
            self.company,
            [self.b2c_OU],
        )
        self.agreement1 = self._create_agreement(self.user1.id, self.main_OU)
        self.agreement2 = self._create_agreement(self.user2.id, self.b2c_OU)

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

    def _create_agreement(self, uid, operating_unit):
        agreement = self.agreement_obj.with_user(uid).create(
            {
                "code": "DA",
                "name": "Demo Agreement",
                "operating_unit_id": operating_unit.id,
            }
        )
        return agreement

    def test_agreement(self):
        # User 2 is only assigned to B2C Operating Unit, and cannot
        # access Agreement for Main Operating Unit.
        agreement_ids = self.agreement_obj.with_user(self.user2.id).search(
            [
                ("id", "=", self.agreement2.id),
                ("operating_unit_id", "=", self.main_OU.id),
            ]
        )
        self.assertEqual(
            agreement_ids.ids,
            [],
            "User 2 should not have access " "to %s" % self.main_OU.name,
        )
        self.assertEqual(self.agreement1.operating_unit_id.id, self.main_OU.id)

    def test_agreement_serviceprofile(self):
        serviceprofile_id = self.serviceprofile_obj.create(
            {
                "name": "Test Agreement Serviceprofile",
                "agreement_id": self.agreement1.id,
                "product_id": self.product_id.id,
            }
        )
        self.assertEqual(serviceprofile_id.agreement_id.operating_unit_id, self.main_OU)
