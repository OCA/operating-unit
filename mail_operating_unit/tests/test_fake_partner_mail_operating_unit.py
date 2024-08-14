# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo_test_helper import FakeModelLoader

from odoo.addons.base.tests.common import BaseCommon


class MailOperatingUnitCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()

        from .models.fake_partner import FakePartner

        cls.loader.update_registry((FakePartner,))

        cls.fake_partner = cls.env["res.partner"].create({"name": "Fake Partner"})
        cls.company = cls.env.ref("base.main_company")
        cls.operating_unit_alias_domain = cls.env["mail.alias.domain"].create(
            {"name": "operating_unit.com"}
        )
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "Operating Unit",
                "code": "OU",
                "company_id": cls.company.id,
                "partner_id": cls.company.partner_id.id,
                "alias_domain_id": cls.operating_unit_alias_domain.id,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()

    def test_mail_thread_with_operating_unit(self):
        """
        Test mail.thread with operating_unit_id field set.

        Ensures that when a mail.thread (represented here by a fake partner)
        is associated with an operating unit,
        the mail sent through this thread uses the alias domain
        associated with the operating unit.
        """
        self.fake_partner.write({"operating_unit_id": self.operating_unit.id})
        message = self.fake_partner.message_post(body="Test")
        self.assertEqual(
            message.record_alias_domain_id, self.operating_unit_alias_domain
        )

    def test_mail_thread_with_false_operating_unit(self):
        """
        Test mail.thread with operating_unit_id field set to False.

        Ensures that when a mail.thread (represented here by a fake partner)
        has no operating unit associated,
        the default mail alias domain is used for the mail sent through this thread.
        """
        self.fake_partner.write({"operating_unit_id": False})
        self.assertFalse(self.fake_partner.operating_unit_id)

        default_alias_domain = self.env["mail.alias.domain"].create(
            {"name": "default.com"}
        )
        self.company.write({"alias_domain_id": default_alias_domain.id})
        self.assertEqual(self.company.alias_domain_id, default_alias_domain)
        user_root = self.env.ref("base.user_admin")
        user_root.operating_unit_ids.unlink()
        self.assertFalse(user_root.operating_unit_ids)
        message = self.fake_partner.message_post(body="Test")
        self.assertEqual(message.record_alias_domain_id.name, default_alias_domain.name)
