# Copyright 2026 Ecosoft Co., Ltd. (https://ecosoft.co.th)
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class ResCompany(models.Model):
    _inherit = "res.company"

    new_user_operating_unit_ids = fields.Many2many(
        comodel_name="operating.unit",
        relation="res_company_new_user_operating_unit_rel",
        column1="company_id",
        column2="operating_unit_id",
        string="Default Allowed Operating Units",
        domain="[('company_id', '=', id)]",
        help="Operating units granted to new users of this company, along with "
        "the default one. If both are empty, new users get the operating unit "
        "of the user creating them.",
    )
    new_user_default_operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        string="Default Operating Unit for New Users",
        domain="[('id', 'in', new_user_operating_unit_ids)]",
    )

    @api.constrains("new_user_operating_unit_ids", "new_user_default_operating_unit_id")
    def _check_new_user_operating_units(self):
        for company in self:
            ous = (
                company.new_user_operating_unit_ids
                | company.new_user_default_operating_unit_id
            )
            if ous.filtered(lambda ou, c=company: ou.company_id != c):
                raise ValidationError(
                    self.env._(
                        "Operating units for new users must belong to "
                        "company %(company)s.",
                        company=company.display_name,
                    )
                )
