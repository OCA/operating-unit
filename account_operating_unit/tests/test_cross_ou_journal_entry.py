# © 2019 ForgeFlow S.L.
# © 2019 Serpent Consulting Services Pvt. Ltd.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.exceptions import UserError
from odoo.tests import tagged
from odoo.tests.common import Form

from . import test_account_operating_unit as test_ou


@tagged("post_install", "-at_install")
class TestCrossOuJournalEntry(test_ou.TestAccountOperatingUnit):
    def setUp(self):
        super().setUp()

    def _check_balance(self, account_id, acc_type="clearing"):
        # Check balance for all operating units
        domain = [("account_id", "=", account_id)]
        balance = self._get_balance(domain)
        self.assertEqual(balance, 0.0, "Balance is 0 for all Operating Units.")
        # Check balance for operating B2B units
        domain = [
            ("account_id", "=", account_id),
            ("operating_unit_id", "=", self.b2b.id),
        ]
        balance = self._get_balance(domain)
        if acc_type == "other":
            self.assertEqual(balance, -100, "Balance is -100 for Operating Unit B2B.")
        else:
            self.assertEqual(balance, 100, "Balance is 100 for Operating Unit B2B.")
        # Check balance for operating B2C units
        domain = [
            ("account_id", "=", account_id),
            ("operating_unit_id", "=", self.b2c.id),
        ]
        balance = self._get_balance(domain)
        if acc_type == "other":
            self.assertEqual(balance, 100.0, "Balance is 100 for Operating Unit B2C.")
        else:
            self.assertEqual(balance, -100.0, "Balance is -100 for Operating Unit B2C.")

    def _get_balance(self, domain):
        """
        Call read_group method and return the balance of particular account.
        """
        aml_rec = self.aml_model.with_user(self.user_id.id).read_group(
            domain, ["debit", "credit", "account_id"], ["account_id"]
        )[0]
        return aml_rec.get("debit", 0) - aml_rec.get("credit", 0)

    def test_cross_ou_journal_entry(self):
        """Test balance of cross OU journal entries.
        Test that when I create a manual journal entry with multiple
        operating units, new cross-operating unit entries are created
        automatically whent the journal entry is posted, ensuring that each
        OU is self-balanced."""
        # Create Journal Entries and check the balance of the account
        # based on different operating units.
        self.company.write(
            {"inter_ou_clearing_account_id": self.inter_ou_account_id.id}
        )
        # Create Journal Entries
        journal_ids = self.journal_model.search(
            [("code", "=", "MISC"), ("company_id", "=", self.company.id)], limit=1
        )
        # get default values of account move
        move_vals = self.move_model.default_get([])
        lines = [
            (
                0,
                0,
                {
                    "name": "Test",
                    "account_id": self.current_asset_account_id.id,
                    "debit": 0,
                    "credit": 100,
                    "operating_unit_id": self.b2b.id,
                },
            ),
            (
                0,
                0,
                {
                    "name": "Test",
                    "account_id": self.current_asset_account_id.id,
                    "debit": 100,
                    "credit": 0,
                    "operating_unit_id": self.b2c.id,
                },
            ),
        ]
        move_vals.update(
            {"journal_id": journal_ids and journal_ids.id, "line_ids": lines}
        )
        move = self.move_model.with_user(self.user_id.id).create(move_vals)
        # Post journal entries
        move.action_post()
        # Check the balance of the account
        self._check_balance(self.current_asset_account_id.id, acc_type="other")
        clearing_account_id = self.company.inter_ou_clearing_account_id.id
        self._check_balance(clearing_account_id, acc_type="clearing")

    def test_journal_no_ou(self):
        """Test journal can not create if use self-balance but not ou in journal"""
        with self.assertRaises(UserError):
            with Form(self.journal_model) as f:
                f.type = "bank"
                f.name = "Test new bank not ou"
                f.code = "testcode"
            f.save()
