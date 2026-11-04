# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.orm.model_classes import add_to_registry

from odoo.addons.base.tests.common import BaseCommon


class MailOperatingUnitCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Odoo 19: register the test model with the standard API
        # (odoo_test_helper is not available for 19.0).
        from .models.fake_thread import FakeThread

        add_to_registry(cls.registry, FakeThread)
        cls.registry._setup_models__(cls.env.cr, [FakeThread._name])
        cls.registry.init_models(
            cls.env.cr, [FakeThread._name], {"models_to_check": True}
        )
        cls.addClassCleanup(cls.registry.__delitem__, FakeThread._name)

        cls.fake_record = cls.env[FakeThread._name].create({"name": "Fake Record"})
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

    def test_mail_thread_with_operating_unit(self):
        """A mail.thread record with an operating unit uses the alias domain
        of that operating unit."""
        self.fake_record.write({"operating_unit_id": self.operating_unit.id})
        message = self.fake_record.message_post(body="Test")
        self.assertEqual(
            message.record_alias_domain_id, self.operating_unit_alias_domain
        )

    def test_mail_thread_with_false_operating_unit(self):
        """A mail.thread record without operating unit uses the default
        alias domain."""
        self.fake_record.write({"operating_unit_id": False})
        self.assertFalse(self.fake_record.operating_unit_id)

        default_alias_domain = self.env["mail.alias.domain"].create(
            {"name": "default.com"}
        )
        self.company.write({"alias_domain_id": default_alias_domain.id})
        self.assertEqual(self.company.alias_domain_id, default_alias_domain)
        user_root = self.env.ref("base.user_admin")
        user_root.operating_unit_ids.unlink()
        self.assertFalse(user_root.operating_unit_ids)
        message = self.fake_record.message_post(body="Test")
        self.assertEqual(message.record_alias_domain_id.name, default_alias_domain.name)
