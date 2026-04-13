# © 2026 BITVAX
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
"""Bug: when a sale order with an Operating Unit is invoiced, the
resulting invoice can land on a journal that does not belong to the
order's OU.

Root cause: ``sale_operating_unit._compute_journal_id`` searches for
the journal with a domain that mixes ``operating_unit_id = <ou>`` and
``operating_unit_id = False`` in the same OR clause, then takes
``limit=1`` without an explicit order. If the database happens to
return a no-OU journal first, the SO's ``journal_id`` is set to it,
the invoice is created with that journal, and
``account_operating_unit._check_journal_operating_unit`` either
raises (when the no-OU journal actually has a different OU) or — more
subtly — silently produces an invoice whose journal does not match
the move's OU.

The fix is to perform two searches: first prefer journals matching
the SO's OU; only fall back to a no-OU journal if no matching one
exists.
"""

from odoo.exceptions import UserError
from odoo.models import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon
from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


@tagged("post_install", "-at_install")
class TestCreateInvoiceJournalOu(AccountTestInvoicingCommon, OperatingUnitCommon):
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
                    Command.link(cls.env.ref("sales_team.group_sale_salesman").id),
                ],
                "assigned_operating_unit_ids": [(6, 0, [cls.b2b.id])],
                "default_operating_unit_id": cls.b2b.id,
                "company_id": cls.company.id,
                "company_ids": [Command.link(cls.company.id)],
            }
        )

        Journal = cls.env["account.journal"].sudo()
        # OU1 sale journal first → lower id → it would be the
        # "default" sale journal Odoo picks when there's no filter.
        cls.sale_journal_ou1 = Journal.create(
            {
                "name": "Sales OU1 (test_invoice_journal)",
                "code": "TIJS1",
                "type": "sale",
                "company_id": cls.company.id,
                "operating_unit_id": cls.ou1.id,
            }
        )
        cls.sale_journal_b2b = Journal.create(
            {
                "name": "Sales B2B (test_invoice_journal)",
                "code": "TIJSB",
                "type": "sale",
                "company_id": cls.company.id,
                "operating_unit_id": cls.b2b.id,
            }
        )

        cls.team_b2b = cls.env["crm.team"].create(
            {
                "name": "B2B Team (test_invoice_journal)",
                "company_id": cls.company.id,
                "operating_unit_id": cls.b2b.id,
                "user_id": cls.user1.id,
            }
        )
        cls.env["crm.team.member"].create(
            {
                "user_id": cls.user1.id,
                "crm_team_id": cls.team_b2b.id,
            }
        )
        cls.user1.invalidate_recordset(["sale_team_id"])

        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product (test_invoice_journal)",
                "list_price": 100.0,
                "type": "consu",
            }
        )

    def test_create_invoice_from_b2b_sale_order_uses_b2b_journal(self):
        env_user1 = self.env(user=self.user1)
        order = env_user1["sale.order"].create(
            {
                "partner_id": self.partner1.id,
                "team_id": self.team_b2b.id,
                "operating_unit_id": self.b2b.id,
                "order_line": [
                    (
                        0,
                        0,
                        {
                            "product_id": self.product.id,
                            "product_uom_qty": 1,
                            "price_unit": 100.0,
                        },
                    )
                ],
            }
        )
        self.assertEqual(order.operating_unit_id, self.b2b)

        order.action_confirm()
        for line in order.order_line:
            line.qty_delivered = line.product_uom_qty

        try:
            invoices = order._create_invoices()
        except UserError as e:
            self.fail(f"Creating invoice from B2B sale order raised UserError: {e}")
        self.assertEqual(len(invoices), 1)
        invoice = invoices[0]
        self.assertEqual(invoice.operating_unit_id, self.b2b)
        self.assertEqual(
            invoice.journal_id.operating_unit_id,
            self.b2b,
            "Invoice journal must belong to B2B (the order's OU).",
        )
