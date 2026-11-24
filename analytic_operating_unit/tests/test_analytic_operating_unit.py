# Copyright 2026 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import Command
from odoo.exceptions import AccessError
from odoo.fields import Domain
from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestAnalyticOperatingUnit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env = cls.env(context=dict(cls.env.context, tracking_disable=True))
        cls.company = cls.env.ref("base.main_company")
        cls.ou1 = cls.env.ref("operating_unit.main_operating_unit")
        cls.b2b = cls.env["operating.unit"].create(
            {
                "name": "B2B",
                "code": "B2B",
                "partner_id": cls.company.partner_id.id,
            }
        )
        plan = cls.env["account.analytic.plan"].create({"name": "OU plan"})
        account_vals = {"plan_id": plan.id, "company_id": cls.company.id}
        cls.account_ou1 = cls.env["account.analytic.account"].create(
            dict(account_vals, name="OU1 account", operating_unit_ids=cls.ou1.ids)
        )
        cls.account_b2b = cls.env["account.analytic.account"].create(
            dict(account_vals, name="B2B account", operating_unit_ids=cls.b2b.ids)
        )
        cls.account_shared = cls.env["account.analytic.account"].create(
            dict(account_vals, name="Shared account")
        )
        cls.accounts = cls.account_ou1 | cls.account_b2b | cls.account_shared
        cls.user = cls._create_user(
            "analytic_ou_user", "operating_unit.group_multi_operating_unit", cls.ou1
        )
        cls.manager = cls._create_user(
            "analytic_ou_manager", "operating_unit.group_manager_operating_unit"
        )

    @classmethod
    def _create_user(cls, login, group_xmlid, operating_units=None):
        groups = cls.env.ref("base.group_user")
        groups |= cls.env.ref("analytic.group_analytic_accounting")
        groups |= cls.env.ref(group_xmlid)
        return cls.env["res.users"].create(
            {
                "name": login,
                "login": login,
                "company_id": cls.company.id,
                "company_ids": [Command.set(cls.company.ids)],
                "group_ids": [Command.set(groups.ids)],
                "assigned_operating_unit_ids": [
                    Command.set(operating_units.ids if operating_units else [])
                ],
            }
        )

    def _visible_accounts(self, user):
        domain = Domain("id", "in", self.accounts.ids)
        return self.env["account.analytic.account"].with_user(user).search(domain)

    def test_user_sees_own_and_shared_accounts(self):
        self.assertEqual(
            self._visible_accounts(self.user),
            self.account_ou1 | self.account_shared,
        )

    def test_user_cannot_read_other_operating_unit_account(self):
        with self.assertRaises(AccessError):
            self.account_b2b.with_user(self.user).check_access("read")

    def test_manager_sees_all_accounts(self):
        self.assertEqual(self._visible_accounts(self.manager), self.accounts)

    def test_new_operating_unit_applies_immediately(self):
        self.user.assigned_operating_unit_ids += self.b2b
        self.assertEqual(self._visible_accounts(self.user), self.accounts)
