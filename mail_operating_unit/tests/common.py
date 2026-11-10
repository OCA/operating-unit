# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.fields import Command
from odoo.orm.model_classes import add_to_registry

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class MailOperatingUnitCommon(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Email Alias Domains: created here so the tests do not depend on
        # demo data (not loaded by default since 19.0)
        AliasDomain = cls.env["mail.alias.domain"]
        cls.ou_alias_domain = AliasDomain.create({"name": "test-main-ou.example.com"})
        cls.b2b_alias_domain = AliasDomain.create({"name": "test-b2b-ou.example.com"})
        cls.b2c_alias_domain = AliasDomain.create({"name": "test-b2c-ou.example.com"})
        cls.ou1.alias_domain_id = cls.ou_alias_domain
        # Since operating_unit 19.0 the B2B/B2C operating units are created by
        # OperatingUnitCommon instead of demo data
        cls.b2b.alias_domain_id = cls.b2b_alias_domain
        cls.b2c.alias_domain_id = cls.b2c_alias_domain
        cls.default_alias_domain = AliasDomain.create(
            {"name": "test-default.example.com"}
        )
        # Company
        cls.company.write({"alias_domain_id": cls.default_alias_domain.id})
        # Users
        cls.user3 = cls._create_user("user_3", cls.grp_ou_multi, cls.company, cls.ou1)
        cls.user3.write(
            {
                "group_ids": [
                    Command.link(cls.env.ref("base.group_partner_manager").id),
                    Command.link(cls.env.ref("base.group_user").id),
                ]
            }
        )
        # Mail objects
        cls.channel_general = cls.env.ref("mail.channel_all_employees")
        # Mail template used by template / alias-domain tests
        cls.mail_template = cls.env["mail.template"].create(
            {
                "name": "Test Template",
                "model_id": cls.env.ref("base.model_res_partner").id,
                "subject": "Test",
                "body_html": "Test",
                "email_from": "admin@example.com",
                "email_to": "{{ object.email or 'test@example.com' }}",
            }
        )


class FakeRecordMailOperatingUnitCommon(BaseCommon):
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
        fake_model = cls.env["ir.model"]._get(FakeThread._name)
        cls.env["ir.model.access"].create(
            {
                "name": "access_mail_ou_fake_thread_user",
                "model_id": fake_model.id,
                "group_id": cls.env.ref("base.group_user").id,
                "perm_read": True,
                "perm_write": True,
                "perm_create": True,
                "perm_unlink": True,
            }
        )

        cls.fake_record = cls.env[FakeThread._name].create(
            {
                "name": "Fake Record",
                "email": "fake@example.com",
            }
        )
        cls.company = cls.env.ref("base.main_company")

        # Alias domains
        cls.operating_unit_alias_domain = cls.env["mail.alias.domain"].create(
            {"name": "operating_unit.com"}
        )
        cls.other_alias_domain = cls.env["mail.alias.domain"].create(
            {"name": "other.com"}
        )
        cls.default_alias_domain = cls.env["mail.alias.domain"].create(
            {"name": "default.com"}
        )
        cls.company.write({"alias_domain_id": cls.default_alias_domain.id})

        # Outgoing mail servers
        cls.mail_server_1 = cls.env["ir.mail_server"].create(
            {
                "name": "Test SMTP 1",
                "smtp_host": "smtp1.example.com",
                "smtp_port": 587,
            }
        )
        cls.mail_server_2 = cls.env["ir.mail_server"].create(
            {
                "name": "Test SMTP 2",
                "smtp_host": "smtp2.example.com",
                "smtp_port": 587,
            }
        )

        # Operating units
        cls.operating_unit = cls.env["operating.unit"].create(
            {
                "name": "Operating Unit",
                "code": "OU",
                "company_id": cls.company.id,
                "partner_id": cls.company.partner_id.id,
                "alias_domain_id": cls.operating_unit_alias_domain.id,
                "mail_server_id": cls.mail_server_1.id,
            }
        )
        cls.other_operating_unit = cls.env["operating.unit"].create(
            {
                "name": "Other Operating Unit",
                "code": "OU2",
                "company_id": cls.company.id,
                "partner_id": cls.company.partner_id.id,
                "alias_domain_id": cls.other_alias_domain.id,
                "mail_server_id": cls.mail_server_2.id,
            }
        )
        cls.shared_operating_unit = cls.env["operating.unit"].create(
            {
                "name": "Shared Operating Unit",
                "code": "OU3",
                "company_id": cls.company.id,
                "partner_id": cls.company.partner_id.id,
                "alias_domain_id": cls.other_alias_domain.id,
                "mail_server_id": cls.mail_server_1.id,
            }
        )

        # Template used for fake record tests
        cls.mail_template = cls.env["mail.template"].create(
            {
                "name": "Test Template",
                "model_id": fake_model.id,
                "subject": "Test",
                "body_html": "Test",
                "email_from": "admin@example.com",
                "email_to": "{{ object.email or 'test@example.com' }}",
                "auto_delete": False,
            }
        )
