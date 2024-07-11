# Copyright 2024 Camptocamp SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.models import Command

from odoo.addons.operating_unit.tests.common import OperatingUnitCommon


class MailOperatingUnitCommon(OperatingUnitCommon):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Email Alias Domain
        cls.ou_alias_domain = cls.env.ref("mail_operating_unit.ou_alias_domain")
        cls.b2c_alias_domain = cls.env.ref("mail_operating_unit.b2b_alias_domain")
        cls.b2b_alias_domain = cls.env.ref("mail_operating_unit.b2c_alias_domain")
        cls.default_alias_domain = cls.env["mail.alias.domain"].create(
            {"name": "default.com"}
        )
        # Company
        cls.company.write({"alias_domain_id": cls.default_alias_domain.id})
        # Users
        # Create User 3 with Main OU and group_multi_operating_unit
        cls.user3 = cls._create_user("user_3", cls.grp_ou_multi, cls.company, cls.ou1)
        # Add following groups to user3: 'Contact Creation'; 'Internal User'
        cls.user3.write(
            {
                "groups_id": [
                    Command.link(cls.env.ref("base.group_partner_manager").id),
                    Command.link(cls.env.ref("base.group_user").id),
                ]
            }
        )
        cls.channel_general = cls.env.ref("mail.channel_all_employees")
