##############################################################################
#
#    Copyright (c) 2019 brain-tec AG (http://www.braintec-group.com)
#    License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
#
##############################################################################

{
    "name": "Mail Operating Unit",
    "summary": "Adds the concept of operating unit (OU) according mail",
    "version": "12.0.1.0.2",
    "author": "brain-tec AG, "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/operating-unit",
    "category": "Purchase Management",
    "depends": ["operating_unit", "mail", "base"],
    "license": "LGPL-3",
    "data": [
        "data/mail_data.xml",
        "security/mail_alias_security.xml",
        "security/mail_template_security.xml",
        "views/operating_unit_views_ext.xml",
        "views/mail_alias_views_ext.xml",
        "views/mail_template_views_ext.xml",
        "views/res_users_view.xml",
        "wizard/mail_compose_message_view_ext.xml",
    ],
    "installable": True,
}
