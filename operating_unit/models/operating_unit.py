# Copyright 2015-TODAY ForgeFlow
# - Jordi Ballester Alomar
# Copyright 2015-TODAY Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class OperatingUnit(models.Model):

    _name = "operating.unit"
    _description = "Operating Unit"

    name = fields.Char(required=True)
    code = fields.Char(required=True)
    active = fields.Boolean(default=True)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        readonly=True,
        default=lambda self: self.env.company,
    )
    partner_id = fields.Many2one("res.partner", "Partner", required=True)
    user_ids = fields.Many2many(
        "res.users",
        "operating_unit_users_rel",
        "operating_unit_id",
        "user_id",
        "Users Allowed",
    )

    _sql_constraints = [
        (
            "code_company_uniq",
            "unique (code,company_id)",
            "The code of the operating unit must " "be unique per company!",
        ),
        (
            "name_company_uniq",
            "unique (name,company_id)",
            "The name of the operating unit must " "be unique per company!",
        ),
    ]

    @api.model
    def name_search(self, name="", args=None, operator="ilike", limit=100):
        # Make a search with default criteria
        names1 = super(models.Model, self).name_search(
            name=name, args=args, operator=operator, limit=limit
        )
        # Make the other search
        names2 = []
        if name:
            domain = [("code", "=ilike", name + "%")]
            if args:
                domain.extend(list(args))
            names2 = self.search(domain, limit=limit).name_get()
        # Merge both results
        return list(set(names1) | set(names2))[:limit]

    def name_get(self):
        res = []
        for ou in self:
            name = ou.name
            if ou.code:
                name = "[{}] {}".format(ou.code, name)
            res.append((ou.id, name))
        return res

    @api.model
    def create(self, values):
        res = super(OperatingUnit, self).create(values)
        res.user_ids += self.env.user
        self.clear_caches()
        return res

    def write(self, vals):
        self.clear_caches()
        return super(OperatingUnit, self).write(vals)
