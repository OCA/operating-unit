# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.models import Command
from odoo.tests import tagged

from .common import TestAccountOperatingUnitCommon


@tagged("post_install", "-at_install")
class TestAccountBankStatementOperatingUnit(TestAccountOperatingUnitCommon):
    def test_00_statement_line_uses_journal_operating_unit(self):
        """Test a statement line applies its journal OU to its move and lines."""
        statement_line = self.env["account.bank.statement.line"].create(
            {
                "amount": 100.0,
                "date": "2026-01-15",
                "journal_id": self.cash_journal_ou1.id,
                "payment_ref": "Statement line with journal",
            }
        )

        self.assertEqual(statement_line.move_id.operating_unit_id, self.ou1)
        self.assertRecordValues(
            statement_line.move_id.line_ids,
            [{"operating_unit_id": self.ou1.id}] * len(statement_line.move_id.line_ids),
        )

    def test_01_statement_line_uses_statement_journal_operating_unit(self):
        """Test a statement-only line resolves and applies the statement journal OU."""
        statement = self.env["account.bank.statement"].create(
            {
                "name": "Operating unit test statement",
                "line_ids": [
                    Command.create(
                        {
                            "amount": 100.0,
                            "date": "2026-01-15",
                            "journal_id": self.cash_journal_ou1.id,
                            "payment_ref": "Initial statement line",
                        }
                    )
                ],
            }
        )
        statement_line = self.env["account.bank.statement.line"].create(
            {
                "amount": 50.0,
                "date": "2026-01-16",
                "payment_ref": "Statement line without journal",
                "statement_id": statement.id,
            }
        )

        self.assertEqual(statement_line.move_id.operating_unit_id, self.ou1)
        self.assertRecordValues(
            statement_line.move_id.line_ids,
            [{"operating_unit_id": self.ou1.id}] * len(statement_line.move_id.line_ids),
        )
