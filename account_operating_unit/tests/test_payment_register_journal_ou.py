# © 2026 BITVAX
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
"""Bug: account.payment.register wizard's available_journal_ids
includes journals from operating units the invoice does not belong to.

A B2B invoice should only offer journals whose operating_unit_id
matches B2B (or no OU). On upstream/18.0 the wizard pulls journals via
``account.journal.search()`` without OU context, so it returns every
sale/cash journal of the company regardless of OU.

The fix is to override
``account.payment.register._get_batch_available_journals`` and filter
the returned set by the operating_unit_id of the invoices in the
batch.
"""

from odoo.models import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


@tagged("post_install", "-at_install")
class TestPaymentRegisterJournalOu(AccountTestInvoicingCommon, OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        (cls.ou1 | cls.b2b | cls.b2c).sudo().write({"company_id": cls.company.id})

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
        cls.purchase_journal_b2b = Journal.create(
            {
                "name": "Vendor Bills B2B (test_pay_reg)",
                "code": "TPRPB",
                "type": "purchase",
                "company_id": cls.company.id,
                "operating_unit_id": cls.b2b.id,
            }
        )
        cls.cash_journal_ou1 = Journal.create(
            {
                "name": "Cash OU1 (test_pay_reg)",
                "code": "TPRC1",
                "type": "cash",
                "company_id": cls.company.id,
                "operating_unit_id": cls.ou1.id,
            }
        )
        cls.cash_journal_b2b = Journal.create(
            {
                "name": "Cash B2B (test_pay_reg)",
                "code": "TPRCB",
                "type": "cash",
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

    def test_payment_register_filters_journals_by_invoice_ou(self):
        invoice = (
            self.env["account.move"]
            .with_context(default_move_type="in_invoice")
            .create(
                {
                    "partner_id": self.partner1.id,
                    "operating_unit_id": self.b2b.id,
                    "invoice_date": "2026-01-01",
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
        invoice.action_post()

        wizard = (
            self.env["account.payment.register"]
            .with_user(self.user1)
            .with_context(
                active_model="account.move",
                active_ids=invoice.ids,
            )
            .create({"journal_id": self.cash_journal_b2b.id})
        )
        available = wizard.available_journal_ids
        self.assertIn(
            self.cash_journal_b2b,
            available,
            "B2B cash journal must be available to pay a B2B invoice.",
        )
        self.assertNotIn(
            self.cash_journal_ou1,
            available,
            "OU1 cash journal must NOT be available when paying a " "B2B invoice.",
        )
