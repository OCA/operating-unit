from odoo.addons.base.tests.common import BaseCommon, Command


class TestAccountBankStatementLine(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Create a partner
        cls.partner = cls.env["res.partner"].create(
            {
                "name": "Test Partner",
                "email": "test@example.com",
            }
        )

        # Create an operating unit
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "Test OU",
                "code": "TEST",
                "partner_id": cls.partner.id,
            }
        )

        # Create accounts
        cls.account_receivable = cls.env["account.account"].create(
            {
                "name": "Test Receivable Account",
                "code": "TEST1",
                "account_type": "asset_receivable",
                "reconcile": True,
            }
        )

        cls.account_revenue = cls.env["account.account"].create(
            {
                "code": "X2020",
                "name": "Product Sales - (test)",
                "account_type": "income",
            }
        )

        # Create tax accounts
        cls.tax_account = cls.env["account.account"].create(
            {
                "name": "Tax Account",
                "code": "TAX",
                "account_type": "liability_current",
                "reconcile": False,
            }
        )

        # Create a journal
        cls.journal = cls.env["account.journal"].create(
            {
                "name": "Test Journal",
                "type": "sale",
                "code": "TESTJ",
                "default_account_id": cls.account_revenue.id,
            }
        )

        cls.currency = cls.env["res.currency"].create(
            {
                "name": "C",
                "symbol": "C",
                "rounding": 0.01,
                "currency_unit_label": "Curr",
                "rate": 1,
            }
        )

        # Get cash basis tax account
        cls.cash_basis_base_account = cls.env["account.account"].create(
            {
                "name": "Cash Basis Base Account",
                "code": "CBBA",
                "account_type": "liability_current",
                "reconcile": False,
            }
        )

        # Create a tax for cash basis tests with required fields
        cls.tax_line = cls.env["account.tax"].create(
            {
                "name": "Test Tax",
                "amount": 15.0,
                "amount_type": "percent",
                "type_tax_use": "sale",
                "tax_exigibility": "on_payment",
                "cash_basis_transition_account_id": cls.cash_basis_base_account.id,
                "invoice_repartition_line_ids": [
                    Command.create(
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    Command.create(
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": cls.tax_account.id,
                        },
                    ),
                ],
                "refund_repartition_line_ids": [
                    Command.create(
                        {
                            "factor_percent": 100,
                            "repartition_type": "base",
                        },
                    ),
                    Command.create(
                        {
                            "factor_percent": 100,
                            "repartition_type": "tax",
                            "account_id": cls.tax_account.id,
                        },
                    ),
                ],
            }
        )

        analytic_plan = cls.env["account.analytic.plan"].create(
            {"name": "Plan with Tax details"}
        )
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {
                "name": "Analytic account with Tax details",
                "plan_id": analytic_plan.id,
                "company_id": False,
            }
        )

        # Create analytic distribution
        cls.analytic_distribution = {str(cls.analytic_account.id): 100}

        # Create a move with balanced entries
        cls.move = cls.env["account.move"].create(
            {
                "name": "Test Move",
                "move_type": "entry",
                "journal_id": cls.journal.id,
                "line_ids": [
                    Command.create(
                        {
                            "name": "Debit Line",
                            "account_id": cls.account_receivable.id,
                            "operating_unit_id": cls.operating_unit.id,
                            "partner_id": cls.partner.id,
                            "debit": 100.0,
                            "credit": 0.0,
                            "amount_currency": 100.0,
                            "currency_id": cls.env.company.currency_id.id,
                            "analytic_distribution": cls.analytic_distribution,
                        },
                    ),
                    Command.create(
                        {
                            "name": "Credit Line",
                            "account_id": cls.account_revenue.id,
                            "operating_unit_id": cls.operating_unit.id,
                            "partner_id": cls.partner.id,
                            "debit": 0.0,
                            "credit": 100.0,
                            "amount_currency": -100.0,
                            "currency_id": cls.env.company.currency_id.id,
                            "analytic_distribution": cls.analytic_distribution,
                        },
                    ),
                ],
            }
        )

    def test_prepare_cash_basis_base_line_vals(self):
        """Test operating unit propagation in cash basis base line"""
        reconcile = self.env["account.partial.reconcile"]
        move_line = self.move.line_ids.filtered(lambda x: x.debit > 0)
        result = reconcile._prepare_cash_basis_base_line_vals(move_line, 100.0, 100.0)

        self.assertEqual(
            result["operating_unit_id"],
            self.operating_unit.id,
            "Operating unit not correctly set on cash basis base line",
        )

    def test_prepare_cash_basis_counterpart_base_line_vals(self):
        """Test operating unit propagation in cash basis counterpart base line"""
        reconcile = self.env["account.partial.reconcile"]
        base_vals = {
            "operating_unit_id": self.operating_unit.id,
            "name": "Test",
            "debit": 100.0,
            "credit": 0.0,
            "account_id": self.account_receivable.id,
            "partner_id": self.partner.id,
            "amount_currency": 100.0,
            "currency_id": self.env.company.currency_id.id,
            "analytic_distribution": self.analytic_distribution,
            "display_type": "cogs",
        }

        result = reconcile._prepare_cash_basis_counterpart_base_line_vals(base_vals)

        self.assertEqual(
            result["operating_unit_id"],
            self.operating_unit.id,
            "Operating unit not correctly set on cash basis counterpart base line",
        )

    def test_prepare_cash_basis_tax_line_vals(self):
        """Test operating unit propagation in cash basis tax line"""
        reconcile = self.env["account.partial.reconcile"]
        move_line = self.move.line_ids.filtered(lambda x: x.debit > 0)
        result = reconcile._prepare_cash_basis_tax_line_vals(move_line, 15.0, 15.0)

        self.assertEqual(
            result["operating_unit_id"],
            self.operating_unit.id,
            "Operating unit not correctly set on cash basis tax line",
        )

    def test_prepare_cash_basis_counterpart_tax_line_vals(self):
        """Test operating unit propagation in cash basis counterpart tax line"""
        reconcile = self.env["account.partial.reconcile"]
        tax_repartition_line = self.tax_line.invoice_repartition_line_ids.filtered(
            lambda x: x.repartition_type == "tax"
        )

        # Ensure all required keys are present in tax_vals
        tax_vals = {
            "operating_unit_id": self.operating_unit.id,
            "name": "Test Tax",
            "debit": 15.0,
            "credit": 0.0,
            "account_id": self.tax_account.id,
            "partner_id": self.partner.id,
            "tax_repartition_line_id": tax_repartition_line.id,
            "analytic_distribution": self.analytic_distribution,
            "amount_currency": 15.0,  # Add the missing key
            "currency_id": self.currency.id,  # Ensure currency_id is set
            "display_type": "tax",
        }
        # Call the method under test
        result = reconcile._prepare_cash_basis_counterpart_tax_line_vals(
            tax_repartition_line, tax_vals
        )

        # Verify the expected result
        self.assertEqual(
            result["operating_unit_id"],
            self.operating_unit.id,
            "Operating unit not correctly set on cash basis counterpart tax line",
        )
