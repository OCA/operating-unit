from unittest.mock import MagicMock

from odoo.tests.common import TransactionCase


class TestReportQwebOperatingUnit(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.ou = cls.env.ref("operating_unit.b2b_operating_unit")
        cls.env.company.report_header = "Company report header"
        cls.ou.report_header = "OU report header"
        cls.mock_user = MagicMock(wraps=cls.env.user)
        cls.mock_user.__contains__ = lambda self, other: True
        cls.mock_user.operating_unit_id = cls.ou

    def test_rendering(self):
        for layout in ("standard", "striped", "bold", "boxed"):
            xmlid = "web.external_layout_%s" % layout
            render_context = dict(
                company=self.env.company,
                o=self.env.user,
            )
            html = (
                self.env["ir.actions.report"]
                ._render_template(
                    xmlid,
                    render_context,
                )
                .decode("utf8")
            )
            self.assertIn(self.env.company.report_header, html)
            html = (
                self.env["ir.actions.report"]
                ._render_template(
                    xmlid,
                    dict(render_context, o=self.mock_user),
                )
                .decode("utf8")
            )
            self.assertIn(self.ou.report_header, html)
