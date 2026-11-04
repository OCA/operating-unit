# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import Command
from odoo.tests import tagged

from .common import TestAccountOperatingUnitCommon


@tagged("post_install", "-at_install")
class TestOuSecurity(TestAccountOperatingUnitCommon):
    def test_security(self):
        """Test Security of Account Operating Unit"""
        # User 2 is only assigned to Operating Unit B2C, and cannot list
        # Journal Entries from Operating Unit B2B.
        move_ids = self.aml_model.with_user(self.user2.id).search(
            [("operating_unit_id", "=", self.b2b.id)]
        )
        self.assertFalse(
            move_ids, "user_2 should not have access to OU %s" % self.b2b.name
        )

    def _get_account(self, account_type):
        return self.account_model.search(
            [("account_type", "=", account_type), ("company_id", "=", self.company.id)],
            limit=1,
        )

    def _create_entry(self, operating_unit, line_operating_unit):
        entry = self.move_model.create(
            {
                "move_type": "entry",
                "journal_id": self.journal_model.search(
                    [("type", "=", "general"), ("company_id", "=", self.company.id)],
                    limit=1,
                ).id,
                "operating_unit_id": operating_unit.id,
                "line_ids": [
                    Command.create(
                        {
                            "account_id": account.id,
                            "debit": debit,
                            "credit": credit,
                        }
                    )
                    for account, debit, credit in (
                        (self._get_account("expense"), 100, 0),
                        (self._get_account("income"), 0, 100),
                    )
                ],
            }
        )
        entry.line_ids.write({"operating_unit_id": line_operating_unit.id})
        return entry

    def test_security_line_follows_entry(self):
        """A line without operating unit is hidden with its entry"""
        entry = self._create_entry(self.b2b, self.env["operating.unit"])
        domain = [("move_id", "=", entry.id)]
        self.assertFalse(self.aml_model.with_user(self.user2).search(domain))
        self.assertEqual(
            self.aml_model.with_user(self.user1).search(domain), entry.line_ids
        )

    def test_security_line_without_entry_operating_unit(self):
        """The line operating unit applies when its entry has none"""
        self.company.ou_is_self_balanced = False
        entry = self._create_entry(self.env["operating.unit"], self.b2b)
        domain = [("move_id", "=", entry.id)]
        self.assertFalse(self.aml_model.with_user(self.user2).search(domain))
        self.assertEqual(
            self.aml_model.with_user(self.user1).search(domain), entry.line_ids
        )
