from unittest.mock import MagicMock

from odoo.tools import is_html_empty

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class TestReportQwebOperatingUnit(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env.company.report_header = "Company report header"
        cls.ou1.report_header = "OU report header"
        cls.mock_user = MagicMock(wraps=cls.env.user)
        cls.mock_user.__contains__ = lambda self, other: True
        cls.mock_user.operating_unit_id = cls.ou1

    def test_rendering(self):
        for layout in ("standard", "striped", "bold", "boxed"):
            xmlid = f"web.external_layout_{layout}"
            render_context = dict(
                company=self.env.company,
                o=self.env.user,
                is_html_empty=is_html_empty,
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
            self.assertIn(self.ou1.report_header, html)

    def test_compute_partner_image(self):
        empty_image = (
            b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC"
            b"0lEQVR42mP8/x8AAwMCAO5WCKsAAAAASUVORK5CYII="
        )
        other_image = (
            b"iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC"
            b"0lEQVR42mNgYAAAAAMAAWgmWQ0AAAAASUVORK5CYII="
        )
        self.ou1.partner_image = empty_image
        self.assertEqual(self.ou1.partner_id.image_1920, empty_image)
        self.ou1.partner_id.image_1920 = other_image
        self.assertEqual(self.ou1.partner_image, other_image)
