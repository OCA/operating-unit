from odoo import fields, models


class OperatingUnitCompanyMapper(models.Model):
    _name = "operating.unit.company.mapping"
    _description = "Create a mapping between OU code prefix and company."
    
    name = fields.Char(string="Name", required=True)
    code_prefix = fields.Char(string="Code Prefix", required=True)
    company_id = fields.Many2one("res.company", string="Company", required=True)
    
    _sql_constraints = [("code_prefix_uniq", "unique (code_prefix)", "Code prefix must be unique.")]