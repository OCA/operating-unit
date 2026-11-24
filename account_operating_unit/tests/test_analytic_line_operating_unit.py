# Copyright 2026 Jarsa
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.tests import tagged

from .common import TestAccountOperatingUnitCommon


@tagged("post_install", "-at_install")
class TestAnalyticLineOperatingUnit(TestAccountOperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        plan = cls.env["account.analytic.plan"].create({"name": "OU plan"})
        cls.analytic_account = cls.env["account.analytic.account"].create(
            {"name": "OU analytic", "plan_id": plan.id, "company_id": cls.company.id}
        )

    def _post_invoice(self, operating_unit):
        vals = self._prepare_invoice(operating_unit.id)
        for command in vals["invoice_line_ids"]:
            command[2]["analytic_distribution"] = {str(self.analytic_account.id): 100}
        invoice = self.move_model.create(vals)
        invoice.invoice_date = invoice.date
        invoice.action_post()
        return invoice

    def test_analytic_lines_get_move_line_operating_unit(self):
        invoice = self._post_invoice(self.b2b)
        analytic_lines = invoice.line_ids.analytic_line_ids
        self.assertEqual(len(analytic_lines), 3)
        self.assertEqual(analytic_lines.operating_unit_id, self.b2b)

    def test_analytic_lines_follow_reposted_operating_unit(self):
        invoice = self._post_invoice(self.b2b)
        invoice.button_draft()
        invoice.operating_unit_id = self.b2c
        invoice.line_ids.operating_unit_id = self.b2c
        invoice.action_post()
        self.assertEqual(invoice.line_ids.analytic_line_ids.operating_unit_id, self.b2c)
