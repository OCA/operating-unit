# Copyright (C) 2019 Open Source Integrators
# Copyright (C) 2019 Serpent Consulting Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = "project.task"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        related="project_id.operating_unit_id",
        string="Operating Unit",
    )
