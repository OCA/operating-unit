# Copyright (C) 2016-2027 CIT Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from ast import literal_eval
from odoo.tests.common import TransactionCase


class TestOperatingUnitWindowActionIsolation(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.ou_a = cls.env["operating.unit"].create(
            {
                "name": "OU A",
                "code": "OUA",
            }
        )

        cls.ou_b = cls.env["operating.unit"].create(
            {
                "name": "OU B",
                "code": "OUB",
            }
        )

        internal_user_group = cls.env.ref("base.group_user")

        cls.user_a = cls.env["res.users"].create(
            {
                "name": "User A",
                "login": "user_a",
                "email": "user_a@example.com",
                "groups_id": [(6, 0, [internal_user_group.id])],
                "default_operating_unit_id": cls.ou_a.id,
                "operating_unit_ids": [(6, 0, [cls.ou_a.id])],
            }
        )

        cls.user_b = cls.env["res.users"].create(
            {
                "name": "User B",
                "login": "user_b",
                "email": "user_b@example.com",
                "groups_id": [(6, 0, [internal_user_group.id])],
                "default_operating_unit_id": cls.ou_b.id,
                "operating_unit_ids": [(6, 0, [cls.ou_b.id])],
            }
        )

        cls.user_without_default_ou = cls.env["res.users"].create(
            {
                "name": "User C",
                "login": "user_c",
                "email": "user_c@example.com",
                "groups_id": [(6, 0, [internal_user_group.id])],
                "operating_unit_ids": [
                    (6, 0, [cls.ou_a.id, cls.ou_b.id])
                ],
            }
        )

        # sale.order contains operating_unit_id
        cls.action_without_domain = cls.env[
            "ir.actions.act_window"
        ].create(
            {
                "name": "Sale Orders",
                "res_model": "sale.order",
                "view_mode": "list,form",
            }
        )

        cls.action_with_domain = cls.env[
            "ir.actions.act_window"
        ].create(
            {
                "name": "Sale Orders With Domain",
                "res_model": "sale.order",
                "view_mode": "list,form",
                "domain": "[('state', '!=', 'cancel')]",
            }
        )

        cls.action_without_ou_field = cls.env[
            "ir.actions.act_window"
        ].create(
            {
                "name": "Countries",
                "res_model": "res.country",
                "view_mode": "list,form",
            }
        )

    def _normalize_domain(self, domain):
        if isinstance(domain, str):
            return literal_eval(domain)
        return domain

    def test_superuser_not_filtered(self):
        """Superuser must not receive OU domain."""
        values = self.action_without_domain.read()[0]

        self.assertFalse(values.get("domain"))

    def test_user_without_default_ou(self):
        """No domain must be injected."""
        values = (
            self.action_without_domain
            .with_user(self.user_without_default_ou)
            .read()[0]
        )

        self.assertFalse(values.get("domain"))

    def test_model_without_operating_unit_field(self):
        """Models without operating_unit_id are ignored."""
        values = (
            self.action_without_ou_field
            .with_user(self.user_a)
            .read()[0]
        )

        self.assertFalse(values.get("domain"))

    def test_action_without_domain(self):
        """OU domain must be created."""
        values = (
            self.action_without_domain
            .with_user(self.user_a)
            .read()[0]
        )

        domain = self._normalize_domain(
            values.get("domain")
        )

        self.assertIn(
            (
                "operating_unit_id",
                "in",
                [False, self.ou_a.id],
            ),
            str(domain),
        )

    def test_ou_a_domain_added(self):
        """User A receives OU A domain."""
        values = (
            self.action_without_domain
            .with_user(self.user_a)
            .read()[0]
        )

        domain = str(values["domain"])

        self.assertIn(
            str(self.ou_a.id),
            domain,
        )

    def test_ou_b_domain_added(self):
        """User B receives OU B domain."""
        values = (
            self.action_without_domain
            .with_user(self.user_b)
            .read()[0]
        )

        domain = str(values["domain"])

        self.assertIn(
            str(self.ou_b.id),
            domain,
        )

    def test_existing_domain_preserved(self):
        """Original action domain must remain."""
        values = (
            self.action_with_domain
            .with_user(self.user_a)
            .read()[0]
        )

        domain = str(values["domain"])

        self.assertIn("state", domain)
        self.assertIn(
            "operating_unit_id",
            domain,
        )

    def test_domain_contains_false_ou(self):
        """Records without OU remain visible."""
        values = (
            self.action_without_domain
            .with_user(self.user_a)
            .read()[0]
        )

        domain = str(values["domain"])

        self.assertIn(
            "[False",
            domain,
        )
