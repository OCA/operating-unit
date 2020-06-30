# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html)

from odoo.tests.common import SavepointCase


class TestAccountOperatingUnitSequence(SavepointCase):
    @classmethod
    def setUpClass(cls):
        super(TestAccountOperatingUnitSequence, cls).setUpClass()
        cls.payment_model = cls.env["account.payment"]
        cls.partner = cls.env["res.partner"].create({"name": "Partner"})
        cls.ou = cls.env.ref("operating_unit.main_operating_unit")
        cls.account_id = cls.env["account.account"].create(
            {
                "name": "Account - Test",
                "code": "account_tes",
                "user_type_id": cls.env.ref("account.data_account_type_liquidity").id,
            }
        )
        cls.journal_id = cls.env["account.journal"].create(
            {
                "name": "Journal - Test",
                "code": "journal_test",
                "type": "cash",
                "default_debit_account_id": cls.account_id.id,
                "default_credit_account_id": cls.account_id.id,
                "operating_unit_id": cls.ou.id,
                "company_id": cls.ou.company_id.id,
            }
        )

    def test_create_sequence(self):
        # Test name != '/'
        payment1 = self.payment_model.create(
            {
                "payment_method_id": self.env.ref(
                    "account.account_payment_method_manual_in"
                ).id,
                "payment_type": "inbound",
                "partner_type": "customer",
                "partner_id": self.partner.id,
                "amount": 100,
                "journal_id": self.journal_id.id,
                "payment_date": "2020-01-01",
                "operating_unit_id": self.ou.id,
                "company_id": self.ou.company_id.id,
            }
        )
        self.assertNotEqual(payment1.name, "/", "Sequence created")
        # Test name 1 != name 2
        payment1_sequence = payment1.name
        payment2 = payment1.copy()
        payment2_sequence = payment2.name
        self.assertNotEqual(
            payment1_sequence, payment2_sequence, "Sequences are different"
        )
