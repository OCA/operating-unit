# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import SavepointCase


class TestSaleOperatingUnitSequence(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestSaleOperatingUnitSequence, cls).setUpClass()
        cls.sale_model = cls.env["sale.order"]
        cls.customer = cls.env["res.partner"].create({"name": "Customer"})

    def test_create_sequence(self):
        # Test name != '/'
        so1 = self.sale_model.create({"partner_id": self.customer.id})
        self.assertNotEqual(so1.name, "/", "Sequence created")
        # Test name 1 != name 2
        so1_sequence = so1.name
        so2 = so1.copy()
        so2_sequence = so2.name
        self.assertNotEqual(so1_sequence, so2_sequence, "Sequences are different")
