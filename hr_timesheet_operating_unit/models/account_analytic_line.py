# SPDX-FileCopyrightText: 2026 Coop IT Easy SC
#
# SPDX-License-Identifier: AGPL-3.0-or-later

from odoo import fields, models


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    operating_unit_id = fields.Many2one(
        comodel_name="operating.unit",
        related="project_id.operating_unit_id",
        string="Operating Unit",
    )
