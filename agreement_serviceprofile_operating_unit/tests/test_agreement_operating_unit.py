# Copyright (C) 2021 Open Source Integrators
# Copyright (C) 2021 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo.addons.agreement_operating_unit.tests.test_agreement_operating_unit import (
    TestAgreementOperatingUnit,
)


class TestAgreementOperatingUnit(TestAgreementOperatingUnit):
    def setUp(self):
        super(TestAgreementOperatingUnit, self).setUp()
        self.serviceprofile_obj = self.env["agreement.serviceprofile"]

    def test_agreement_serviceprofile(self):
        serviceprofile_id = self.serviceprofile_obj.create(
            {
                "name": "Test Agreement Serviceprofile",
                "agreement_id": self.agreement1.id,
                "product_id": self.product_id.id,
            }
        )
        self.assertEqual(serviceprofile_id.agreement_id.operating_unit_id, self.main_OU)
