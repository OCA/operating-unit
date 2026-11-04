# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.fields import Command

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
        # Create User 3 with Main OU and group_multi_operating_unit
        cls.user3 = cls._create_user("user_3", cls.grp_ou_multi, cls.company, cls.ou1)
        # Add following groups to user3: 'Contact Creation'; 'Internal User'
        cls.user3.write(
            {
                "group_ids": [
                    Command.link(cls.env.ref("base.group_partner_manager").id),
                    Command.link(cls.env.ref("base.group_user").id),
                ]
            }
        )
        cls.channel_general = cls.env.ref("mail.channel_all_employees")
