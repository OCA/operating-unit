# © 2026 BITVAX
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
"""Bug: account.move._onchange_operating_unit raises AccessError when
the journal currently set on the move belongs to an Operating Unit the
acting user cannot read.

This happens because the handler reads ``self.journal_id.type`` and
``self.journal_id.operating_unit_id`` without ``sudo()``. The
account_operating_unit security rule
``ir_rule_account_journal_allowed_operating_units`` denies the read,
and Odoo raises AccessError.

The fix is to use ``.sudo()`` for those two attribute reads. The
journal still gets selected respecting OU because the search done
later filters by operating_unit_id afterwards.
"""

from odoo.exceptions import AccessError
from odoo.models import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


@tagged("post_install", "-at_install")
class TestOnchangeOperatingUnitAccess(AccountTestInvoicingCommon, OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        # Move demo OUs into the test company
        (cls.ou1 | cls.b2b | cls.b2c).sudo().write({"company_id": cls.company.id})

        # The test admin user needs full OU access for setup
        cls.env.user.sudo().write(
            {
                "groups_id": [
                    Command.link(
                        cls.env.ref("operating_unit.group_manager_operating_unit").id
                    ),
                ],
                "operating_unit_ids": [
                    Command.link(cls.ou1.id),
                    Command.link(cls.b2b.id),
                ],
                "default_operating_unit_id": cls.ou1.id,
                "company_ids": [Command.link(cls.company.id)],
                "company_id": cls.company.id,
            }
        )

        # user1 is restricted to B2B only — REMOVES the manager group
        # so its computed operating_unit_ids is restricted by
        # assigned_operating_unit_ids and the security rule actually
        # bites.
        cls.user1.write(
            {
                "groups_id": [
                    (
                        3,
                        cls.env.ref("operating_unit.group_manager_operating_unit").id,
                    ),
                    Command.link(
                        cls.env.ref("operating_unit.group_multi_operating_unit").id
                    ),
                    Command.link(cls.env.ref("account.group_account_invoice").id),
                ],
                "assigned_operating_unit_ids": [(6, 0, [cls.b2b.id])],
                "default_operating_unit_id": cls.b2b.id,
                "company_id": cls.company.id,
                "company_ids": [Command.link(cls.company.id)],
            }
        )

        Journal = cls.env["account.journal"].sudo()
        cls.purchase_journal_ou1 = Journal.create(
            {
                "name": "Vendor Bills OU1 (test_onchange)",
                "code": "TONP1",
                "type": "purchase",
                "company_id": cls.company.id,
                "operating_unit_id": cls.ou1.id,
            }
        )
        cls.purchase_journal_b2b = Journal.create(
            {
                "name": "Vendor Bills B2B (test_onchange)",
                "code": "TONPB",
                "type": "purchase",
                "company_id": cls.company.id,
                "operating_unit_id": cls.b2b.id,
            }
        )

        cls.expense_account = cls.env["account.account"].search(
            [
                ("account_type", "=", "expense"),
                ("company_ids", "in", cls.company.ids),
            ],
            limit=1,
        )

    def test_onchange_operating_unit_no_access_error(self):
        """user1 (B2B-only) calls _onchange_operating_unit on an
        invoice that they CAN read (operating_unit_id = b2b) but
        whose journal_id points to a journal user1 CANNOT read
        (operating_unit_id = ou1). This is the production scenario:
        a draft move that was previously linked to a journal the
        current user lost access to. Without the sudo() fix the
        handler raises AccessError reading journal.type.
        """
        # Create the invoice as admin so we can place it in B2B
        # (so user1 can read it) but force the journal to OU1
        # (so user1 cannot read the journal). This bypasses the
        # _check_journal_operating_unit constraint by using sudo()
        # on the create.
        invoice = (
            self.env["account.move"]
            .sudo()
            .with_context(default_move_type="in_invoice")
            .create(
                {
                    "partner_id": self.partner1.id,
                    "operating_unit_id": self.b2b.id,
                    "journal_id": self.purchase_journal_b2b.id,
                    "invoice_line_ids": [
                        (
                            0,
                            0,
                            {
                                "name": "Line",
                                "quantity": 1,
                                "price_unit": 100.0,
                                "account_id": self.expense_account.id,
                                "tax_ids": [],
                            },
                        )
                    ],
                }
            )
        )
        # Now sneak the OU1 journal onto the move via raw SQL to
        # bypass _check_journal_operating_unit. This simulates a
        # legacy / migrated move that ended up in this inconsistent
        # state and the user is trying to fix it via the form.
        self.env.cr.execute(
            "UPDATE account_move SET journal_id = %s WHERE id = %s",
            (self.purchase_journal_ou1.id, invoice.id),
        )
        invoice.invalidate_recordset(["journal_id"])

        # Sanity: user1 can read the move (it's in B2B).
        invoice.with_user(self.user1).read(["operating_unit_id"])
        # Sanity: user1 cannot read the OU1 journal directly.
        with self.assertRaises(AccessError):
            self.purchase_journal_ou1.with_user(self.user1).type  # noqa: B018

        # The actual repro: trigger the onchange as user1.
        invoice_as_user1 = invoice.with_user(self.user1)
        try:
            invoice_as_user1._onchange_operating_unit()
        except AccessError as e:
            self.fail(
                f"user1 (B2B only) hit AccessError on " f"_onchange_operating_unit: {e}"
            )
