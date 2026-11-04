# Copyright 2026 Aures TIC - Jordi Aura
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from datetime import timedelta

from odoo import fields
from odoo.fields import Command
from odoo.tests import tagged

from odoo.addons.account.tests.common import AccountTestInvoicingCommon


@tagged("post_install", "-at_install")
class TestReportOperatingUnit(AccountTestInvoicingCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.user.write(
            {
                "group_ids": [
                    Command.link(
                        cls.env.ref("operating_unit.group_manager_operating_unit").id
                    )
                ],
            }
        )
        cls.ou_a = cls._create_operating_unit("OU A", "OUA")
        cls.ou_b = cls._create_operating_unit("OU B", "OUB")
        cls.env.user.operating_unit_ids = [
            Command.link(cls.ou_a.id),
            Command.link(cls.ou_b.id),
        ]
        cls.today = fields.Date.context_today(cls.env.user)
        cls.yesterday = cls.today - timedelta(days=1)
        cls.date_from = cls.today - timedelta(days=10)
        cls.receivable = cls.company_data["default_account_receivable"]
        cls.invoice_a = cls._create_invoice(cls.ou_a, 100.0)
        cls.invoice_b = cls._create_invoice(cls.ou_b, 200.0)
        cls.cases = (
            (cls.ou_a, cls.invoice_a),
            (cls.ou_b, cls.invoice_b),
            (cls.env["operating.unit"], cls.invoice_a | cls.invoice_b),
        )

    @classmethod
    def _create_operating_unit(cls, name, code):
        return cls.env["operating.unit"].create(
            {
                "name": name,
                "code": code,
                "partner_id": cls.company.partner_id.id,
                "company_id": cls.company.id,
            }
        )

    @classmethod
    def _create_invoice(cls, operating_unit, price):
        invoice = cls.env["account.move"].create(
            {
                "move_type": "out_invoice",
                "partner_id": cls.partner_a.id,
                "invoice_date": cls.date_from,
                "journal_id": cls.company_data["default_journal_sale"].id,
                "operating_unit_id": operating_unit.id,
                "invoice_line_ids": [
                    Command.create(
                        {
                            "name": "Test",
                            "quantity": 1.0,
                            "price_unit": price,
                            "account_id": cls.company_data[
                                "default_account_revenue"
                            ].id,
                            "tax_ids": [Command.set(cls.tax_sale_a.ids)],
                        }
                    )
                ],
            }
        )
        invoice.action_post()
        return invoice

    @classmethod
    def _pay_today(cls, invoice):
        """Reconcile the invoice today, so it is still open at yesterday's date."""
        payment = cls.env["account.move"].create(
            {
                "move_type": "entry",
                "date": cls.today,
                "journal_id": cls.company_data["default_journal_misc"].id,
                "operating_unit_id": invoice.operating_unit_id.id,
                "line_ids": [
                    Command.create(
                        {
                            "account_id": cls.receivable.id,
                            "partner_id": invoice.partner_id.id,
                            "credit": invoice.amount_total,
                        }
                    ),
                    Command.create(
                        {
                            "account_id": cls.company_data["default_account_assets"].id,
                            "debit": invoice.amount_total,
                        }
                    ),
                ],
            }
        )
        payment.action_post()
        (invoice.line_ids | payment.line_ids).filtered(
            lambda line: line.account_id == cls.receivable
        ).reconcile()

    def _report_values(self, report_name, wizard_model, vals, operating_units):
        wizard = self.env[wizard_model].create(
            dict(
                vals,
                company_id=self.company.id,
                operating_unit_ids=[Command.set(operating_units.ids)],
            )
        )
        if "receivable_accounts_only" in vals:
            wizard.onchange_type_accounts_only()
        # Same serialization as when the report is printed from the wizard
        data = json.loads(json.dumps(wizard._prepare_report_data(), default=str))
        self.assertEqual(data["operating_unit_ids"], operating_units.ids)
        return self.env[
            f"report.account_financial_report.{report_name}"
        ]._get_report_values(wizard, data)

    def test_trial_balance(self):
        vals = {"date_from": self.date_from, "date_to": self.today}
        for ous, invoices in self.cases:
            res = self._report_values(
                "trial_balance", "trial.balance.report.wizard", vals, ous
            )
            self.assertAlmostEqual(
                res["total_amount"][self.receivable.id]["debit"],
                sum(invoices.mapped("amount_total")),
            )

    def test_general_ledger(self):
        vals = {"date_from": self.date_from, "date_to": self.today}
        for ous, invoices in self.cases:
            res = self._report_values(
                "general_ledger", "general.ledger.report.wizard", vals, ous
            )
            account = next(
                acc for acc in res["general_ledger"] if acc["id"] == self.receivable.id
            )
            self.assertAlmostEqual(
                account["fin_bal"]["debit"], sum(invoices.mapped("amount_total"))
            )

    def test_open_items(self):
        vals = {"target_move": "posted", "receivable_accounts_only": True}
        for ous, invoices in self.cases:
            res = self._report_values(
                "open_items",
                "open.items.report.wizard",
                dict(vals, date_at=self.today),
                ous,
            )
            self.assertAlmostEqual(
                res["total_amount"][self.receivable.id]["residual"],
                sum(invoices.mapped("amount_residual")),
            )
        self._pay_today(self.invoice_a)
        self._pay_today(self.invoice_b)
        for ous, invoices in self.cases:
            res = self._report_values(
                "open_items",
                "open.items.report.wizard",
                dict(vals, date_at=self.yesterday),
                ous,
            )
            self.assertAlmostEqual(
                res["total_amount"][self.receivable.id]["residual"],
                sum(invoices.mapped("amount_total")),
            )

    def test_aged_partner_balance(self):
        vals = {"target_move": "posted", "receivable_accounts_only": True}
        self._pay_today(self.invoice_a)
        self._pay_today(self.invoice_b)
        for ous, invoices in self.cases:
            res = self._report_values(
                "aged_partner_balance",
                "aged.partner.balance.report.wizard",
                dict(vals, date_at=self.yesterday),
                ous,
            )
            account = next(
                acc
                for acc in res["aged_partner_balance"]
                if acc["id"] == self.receivable.id
            )
            self.assertAlmostEqual(
                account["residual"], sum(invoices.mapped("amount_total"))
            )

    def test_journal_ledger(self):
        journal = self.company_data["default_journal_sale"]
        vals = {
            "date_from": self.date_from,
            "date_to": self.today,
            "journal_ids": [Command.set(journal.ids)],
            "move_target": "posted",
        }
        for ous, invoices in self.cases:
            res = self._report_values(
                "journal_ledger", "journal.ledger.report.wizard", vals, ous
            )
            journal_data = next(
                jd for jd in res["Journal_Ledgers"] if jd["id"] == journal.id
            )
            self.assertAlmostEqual(
                journal_data["debit"], sum(invoices.mapped("amount_total"))
            )

    def test_vat_report(self):
        vals = {
            "date_from": self.date_from,
            "date_to": self.today,
            "based_on": "taxgroups",
            "tax_detail": True,
            "target_move": "posted",
        }
        for ous, invoices in self.cases:
            res = self._report_values("vat_report", "vat.report.wizard", vals, ous)
            # Sales taxes are reported with negative sign
            self.assertAlmostEqual(
                -sum(group["tax"] for group in res["vat_report"]),
                sum(invoices.mapped("amount_tax")),
            )
