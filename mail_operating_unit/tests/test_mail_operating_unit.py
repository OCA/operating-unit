# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from .common import MailOperatingUnitCommon


class TestMailOperatingUnit(MailOperatingUnitCommon):
    def test_mail_template_with_operating_unit(self):
        """
        Test mail.template with operating_unit_id field set.

        Ensures that when a mail is sent using a mail.template
        with an operating_unit_id,
        the mail.alias.domain associated with that operating unit is correctly used.
        """
        template = self.env["mail.template"].create(
            {
                "name": "Test Template",
                "model_id": self.env.ref("base.model_res_partner").id,
                "subject": "Test",
                "body_html": "Test",
                "operating_unit_id": self.ou1.id,
            }
        )
        mail_id = template.send_mail(self.partner1.id)
        mail = self.env["mail.mail"].browse(mail_id)
        self.assertEqual(mail.record_alias_domain_id, self.ou_alias_domain)

    def test_user_single_operating_unit(self):
        """
        Test for user with a single operating unit.

        Ensures that when a user with exactly one operating unit sends an email,
        the mail.alias.domain associated with that operating unit is used.
        """
        self.b2c.write({"alias_domain_id": self.b2c_alias_domain.id})
        self.user3.write({"operating_unit_ids": [(6, 0, [self.b2c.id])]})

        message = self.channel_general.with_user(self.user3).message_post(
            body="Test",
        )
        self.assertEqual(message.record_alias_domain_id, self.b2c_alias_domain)

    def test_user_no_operating_units(self):
        """
        Test for user with no operating units.

        Ensures that when a user has no operating units,
        the default mail.alias.domain computation
        is used for emails sent by the user.
        """
        self.user3.write({"operating_unit_ids": False})
        message = self.channel_general.with_user(self.user3).message_post(
            body="Test",
        )
        self.assertEqual(message.record_alias_domain_id, self.default_alias_domain)

    def test_user_multiple_operating_units_same_domain(self):
        """
        Test for user with multiple operating units having the same domain.

        Ensures that when a user belongs to multiple operating units
        that all have the same mail.alias.domain,
        this common domain is used for emails sent by the user.
        """
        self.b2b.write({"alias_domain_id": self.ou_alias_domain.id})
        self.b2c.write({"alias_domain_id": self.ou_alias_domain.id})
        self.user3.write({"operating_unit_ids": [(6, 0, [self.b2b.id, self.b2c.id])]})
        message = self.channel_general.with_user(self.user3).message_post(
            body="Test",
        )
        self.assertEqual(message.record_alias_domain_id, self.ou_alias_domain)

    def test_user_multiple_operating_units_different_domains(self):
        """
        Test for user with multiple operating units having different domains.

        Ensures that when a user is associated with multiple operating units
        with different mail.alias.domain,
        the default computation for mail.alias.domain is used.
        """
        self.user3.write({"operating_unit_ids": [(6, 0, [self.b2b.id, self.b2c.id])]})
        message = self.channel_general.with_user(self.user3).message_post(
            body="Test",
        )
        self.assertEqual(message.record_alias_domain_id, self.default_alias_domain)
