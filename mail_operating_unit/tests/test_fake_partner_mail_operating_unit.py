# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.models import Command

from .common import FakePartnerMailOperatingUnitCommon


class TestFakePartnerMailOperatingUnit(FakePartnerMailOperatingUnitCommon):
    def test_00_mail_thread_with_operating_unit(self):
        """Test mail.thread with operating_unit_id field set.

        Ensures that when a mail.thread (represented here by a fake partner)
        is associated with an operating unit,
        the mail sent through this thread uses the alias domain
        associated with the operating unit.
        """
        self.fake_partner.write({"operating_unit_id": self.operating_unit.id})
        message = self.fake_partner.message_post(body="Test")
        self.assertEqual(
            message.record_alias_domain_id,
            self.operating_unit_alias_domain,
        )

    def test_01_mail_thread_with_false_operating_unit(self):
        """Test mail.thread with operating_unit_id field set to False.

        Ensures that when a mail.thread (represented here by a fake partner)
        has no operating unit associated,
        the default mail alias domain is used for the mail sent through this thread.
        """
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [Command.clear()],
            }
        )
        self.assertFalse(self.fake_partner.operating_unit_id)
        user_root = self.env.ref("base.user_admin")
        user_root.operating_unit_ids.unlink()
        self.assertFalse(user_root.operating_unit_ids)
        message = self.fake_partner.message_post(body="Test")
        self.assertEqual(message.record_alias_domain_id, self.default_alias_domain)

    def test_02_mail_thread_with_single_operating_unit_ids(self):
        """Use the record alias domain when one ``operating_unit_ids`` is set."""
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [Command.set([self.operating_unit.id])],
            }
        )
        message = self.fake_partner.message_post(body="Test")
        self.assertEqual(
            message.record_alias_domain_id,
            self.operating_unit_alias_domain,
        )

    def test_03_mail_thread_with_multiple_operating_unit_ids(self):
        """Fallback when multiple ``operating_unit_ids`` are set."""
        user_root = self.env.ref("base.user_admin")
        user_root.operating_unit_ids.unlink()
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [
                    Command.set([self.operating_unit.id, self.other_operating_unit.id])
                ],
            }
        )
        message = self.fake_partner.message_post(body="Test")
        self.assertEqual(message.record_alias_domain_id, self.default_alias_domain)

    def test_04_mail_thread_with_single_operating_unit_ids_without_alias_domain(self):
        """Fallback when the single record OU has no alias domain."""
        user_root = self.env.ref("base.user_admin")
        user_root.operating_unit_ids.unlink()
        self.other_operating_unit.alias_domain_id = False
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [Command.set([self.other_operating_unit.id])],
            }
        )
        message = self.fake_partner.message_post(body="Test")

        self.assertEqual(message.record_alias_domain_id, self.default_alias_domain)

    def test_05_template_mail_server_keeps_priority(self):
        """Template mail server must remain the highest priority."""
        self.mail_template.write({"mail_server_id": self.mail_server_2.id})
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [Command.set([self.operating_unit.id])],
            }
        )
        mail_id = self.mail_template.send_mail(self.fake_partner.id, force_send=False)
        mail = self.env["mail.mail"].browse(mail_id)
        self.assertEqual(mail.mail_server_id, self.mail_server_2)

    def test_06_record_single_operating_unit_ids_mail_server(self):
        """Use the record OU mail server when exactly one OU is set."""
        self.mail_template.write({"mail_server_id": False})
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [Command.set([self.operating_unit.id])],
            }
        )
        mail_id = self.mail_template.send_mail(
            self.fake_partner.id,
            force_send=False,
        )
        mail = self.env["mail.mail"].browse(mail_id)
        mail.send()
        self.assertEqual(mail.mail_server_id, self.mail_server_1)

    def test_07_record_operating_unit_ids_shared_mail_server(self):
        """Use the shared server when all record OUs point to the same one."""
        self.mail_template.write({"mail_server_id": False})
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [
                    Command.set([self.operating_unit.id, self.shared_operating_unit.id])
                ],
            }
        )
        mail_id = self.mail_template.send_mail(
            self.fake_partner.id,
            force_send=False,
        )
        mail = self.env["mail.mail"].browse(mail_id)
        mail.send()
        self.assertEqual(mail.mail_server_id, self.mail_server_1)

    def test_08_record_operating_unit_ids_different_mail_servers(self):
        """Fallback when record OUs do not share the same outgoing mail server."""
        self.mail_template.write({"mail_server_id": False})
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [
                    Command.set([self.operating_unit.id, self.other_operating_unit.id])
                ],
            }
        )
        mail_id = self.mail_template.send_mail(self.fake_partner.id, force_send=False)
        mail = self.env["mail.mail"].browse(mail_id)
        self.assertFalse(mail.mail_server_id)

    def test_09_record_operating_unit_ids_different_servers_use_default_ou(self):
        """Use the current user's default OU when record OUs have different servers."""
        self.fake_partner.write(
            {
                "operating_unit_id": False,
                "operating_unit_ids": [
                    Command.set([self.operating_unit.id, self.other_operating_unit.id])
                ],
            }
        )
        # ``res.users._get_default_operating_unit()`` relies on
        # ``default_operating_unit_id`` first, then on
        # ``assigned_operating_unit_ids`` as fallback.
        # Set both explicitly to make the test deterministic.
        self.env.user.write(
            {
                "assigned_operating_unit_ids": [
                    Command.set([self.operating_unit.id, self.other_operating_unit.id])
                ],
                "default_operating_unit_id": self.other_operating_unit.id,
            }
        )
        self.assertEqual(
            self.env.user._get_default_operating_unit(),
            self.other_operating_unit,
        )
        mail_id = self.mail_template.send_mail(
            self.fake_partner.id,
            force_send=False,
        )
        mail = self.env["mail.mail"].browse(mail_id)
        # When multiple OUs are present on the record
        # and they do not share the same server,
        # the default OU of the current user is used.
        mail.send()
        self.assertEqual(mail.mail_server_id, self.mail_server_2)
