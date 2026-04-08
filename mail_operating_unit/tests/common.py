# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo_test_helper import FakeModelLoader

from odoo.models import Command

from odoo.addons.base.tests.common import BaseCommon
from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class MailOperatingUnitCommon(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Email Alias Domains
        cls.ou_alias_domain = cls.env.ref("mail_operating_unit.ou_alias_domain")
        cls.b2c_alias_domain = cls.env.ref("mail_operating_unit.b2c_alias_domain")
        cls.b2b_alias_domain = cls.env.ref("mail_operating_unit.b2b_alias_domain")
        cls.default_alias_domain = cls.env["mail.alias.domain"].create(
            {"name": "default.com"}
        )
        # Company
        cls.company.write({"alias_domain_id": cls.default_alias_domain.id})
        # Users
        cls.user3 = cls._create_user("user_3", cls.grp_ou_multi, cls.company, cls.ou1)
        cls.user3.write(
            {
                "groups_id": [
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


class FakePartnerMailOperatingUnitCommon(BaseCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.loader = FakeModelLoader(cls.env, cls.__module__)
        cls.loader.backup_registry()

        from .models.fake_partner import FakePartner

        cls.loader.update_registry((FakePartner,))

        cls.fake_partner = cls.env["res.partner"].create(
            {
                "name": "Fake Partner",
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

        # Template used for fake partner tests
        cls.mail_template = cls.env["mail.template"].create(
            {
                "name": "Test Template",
                "model_id": cls.env.ref("base.model_res_partner").id,
                "subject": "Test",
                "body_html": "Test",
                "email_from": "admin@example.com",
                "email_to": "{{ object.email or 'test@example.com' }}",
                "auto_delete": False,
            }
        )

    @classmethod
    def tearDownClass(cls):
        cls.loader.restore_registry()
        super().tearDownClass()
