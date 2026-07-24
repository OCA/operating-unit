# Copyright 2020 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo.tests.common import TransactionCase


class TestSaleOperatingUnitSequence(TransactionCase):
    @classmethod
    def setUpClass(cls):
        """Set up test data for sale operating unit sequence tests."""
        super(TestSaleOperatingUnitSequence, cls).setUpClass()
        cls.sale_model = cls.env["sale.order"]
        cls.customer = cls.env["res.partner"].create({"name": "Customer"})

    def test_create_sequence(self):
        """Test that sale order creation uses and increments sequences correctly."""
        so1 = self.sale_model.create({"partner_id": self.customer.id})
        self.assertNotEqual(so1.name, "/", "Sequence created")
        so1_sequence = so1.name
        so2 = so1.copy()
        so2_sequence = so2.name
        self.assertNotEqual(so1_sequence, so2_sequence, "Sequences are different")

    def test_create_sequence_operating_unit_id_absent_from_vals(self):
        """The OU's sale sequence must apply even when operating_unit_id is
        absent from create() vals - e.g. because the field is hidden for a
        user without the "Multiple Operating Units" permission, or because
        the order was created programmatically without passing it. In that
        case it must be resolved from the field's own default instead."""
        sequence = self.env["ir.sequence"].create(
            {
                "name": "OU Sale Sequence",
                "code": "sale.order.ou.test",
                "prefix": "OUSO-",
                "padding": 3,
            }
        )
        operating_unit = self.env["operating.unit"].create(
            {
                "name": "Test OU",
                "code": "TESTOU",
                "partner_id": self.customer.id,
                "sale_sequence_id": sequence.id,
            }
        )
        user = self.env["res.users"].create(
            {
                "name": "Single OU Salesperson",
                "login": "single_ou_salesperson_base@example.com",
                "email": "single_ou_salesperson_base@example.com",
                "groups_id": [
                    (4, self.env.ref("sales_team.group_sale_salesman").id),
                ],
                "assigned_operating_unit_ids": [(6, 0, [operating_unit.id])],
                "default_operating_unit_id": operating_unit.id,
            }
        )
        self.assertFalse(
            user.has_group("operating_unit.group_multi_operating_unit"),
            "Test user must not have the Multiple Operating Units permission",
        )
        so = (
            self.sale_model.with_user(user)
            .with_company(operating_unit.company_id)
            .create(
                {
                    "partner_id": self.customer.id,
                    # Avoid interference from the unrelated team/OU
                    # consistency constraint (sale_operating_unit): this test
                    # is only about the sequence/OU default resolution.
                    "team_id": False,
                }
            )
        )
        self.assertEqual(so.operating_unit_id, operating_unit)
        self.assertTrue(so.name.startswith("OUSO-"))

    def test_create_sequence_operating_unit_id_explicit_false(self):
        """When the caller explicitly passes operating_unit_id=False, that
        must be respected as "no operating unit" rather than treated the
        same as the key being absent (which would fall back to the field's
        default)."""
        sequence = self.env["ir.sequence"].create(
            {
                "name": "OU Sale Sequence",
                "code": "sale.order.ou.explicit.false.test",
                "prefix": "OUFALSE-",
                "padding": 3,
            }
        )
        operating_unit = self.env["operating.unit"].create(
            {
                "name": "Test OU",
                "code": "TESTOU2",
                "partner_id": self.customer.id,
                "sale_sequence_id": sequence.id,
            }
        )
        user = self.env["res.users"].create(
            {
                "name": "Single OU Salesperson",
                "login": "single_ou_salesperson_false@example.com",
                "email": "single_ou_salesperson_false@example.com",
                "groups_id": [
                    (4, self.env.ref("sales_team.group_sale_salesman").id),
                ],
                "assigned_operating_unit_ids": [(6, 0, [operating_unit.id])],
                "default_operating_unit_id": operating_unit.id,
            }
        )
        so = (
            self.sale_model.with_user(user)
            .with_company(operating_unit.company_id)
            .create(
                {
                    "partner_id": self.customer.id,
                    "team_id": False,
                    "operating_unit_id": False,
                }
            )
        )
        self.assertFalse(so.operating_unit_id)
        self.assertFalse(so.name.startswith("OUFALSE-"))
