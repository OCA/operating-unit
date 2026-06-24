# Copyright 2026 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.models import Command

from odoo.addons.base.tests.common import MockSmtplibCase

from .common import FakePartnerMailOperatingUnitCommon


class TestSmtpServerSelection(FakePartnerMailOperatingUnitCommon, MockSmtplibCase):
    """Verify which SMTP server is actually used when sending mail with an OU.

    Companion to ``TestFakePartnerMailOperatingUnit``, which tests the OU
    resolution logic and the ``mail.mail.mail_server_id`` DB field assignment.
    That class does not verify which SMTP server is actually connected to,
    because Odoo's test mode makes ``ir.mail_server.connect()`` return ``None``
    immediately regardless of the ``mail_server_id`` argument.

    This class uses ``MockSmtplibCase`` to disable that shortcut and intercept
    the real arguments passed to ``connect()``, making it possible to assert
    that the SMTP session is opened on the expected server.

    The scenario under test is a priority conflict: two outgoing mail servers
    coexist, one being a high-priority catch-all (lower ``sequence``) that
    ``_find_mail_server()`` would select by default, and a lower-priority one
    that is the OU's configured server.  The OU server must win.
    """

    def setUp(self):
        super().setUp()
        # mail_server_2: high-priority catch-all (sequence=1)
        # mail_server_1: OU's server (sequence=10, lower priority)
        self.mail_server_2.write({"sequence": 1})
        self.mail_server_1.write({"sequence": 10})
        self.mail_template.write({"mail_server_id": False})

    def test_00_ou_server_used_before_smtp_grouping(self):
        """When an OU is set, its mail server must be used for the SMTP session."""
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [Command.set([self.operating_unit.id])],
            }
        )
        mail_id = self.mail_template.send_mail(self.fake_partner.id, force_send=False)
        mail = self.env["mail.mail"].browse(mail_id)

        with self.mock_smtplib_connection():
            mail.send()

        self.connect_mocked.assert_called_once()
        _, call_kwargs = self.connect_mocked.call_args
        self.assertEqual(
            call_kwargs.get("mail_server_id"),
            self.mail_server_1.id,
            "SMTP session must be opened on the OU mail server, not the catch-all",
        )
        self.assertEqual(mail.mail_server_id, self.mail_server_1)

    def test_01_no_ou_uses_default_server_selection(self):
        """Without an OU, the standard server selection applies (catch-all wins)."""
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [Command.clear()],
            }
        )
        mail_id = self.mail_template.send_mail(self.fake_partner.id, force_send=False)
        mail = self.env["mail.mail"].browse(mail_id)

        with self.mock_smtplib_connection():
            mail.send()

        self.connect_mocked.assert_called_once()
        _, call_kwargs = self.connect_mocked.call_args
        self.assertEqual(
            call_kwargs.get("mail_server_id"),
            self.mail_server_2.id,
            "Without an OU, the highest-priority catch-all server must be used",
        )
