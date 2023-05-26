# Copyright 2015-19 ForgeFlow S.L. -
# Jordi Ballester Alomar
# Copyright 2015-19 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# Copyright 2018-19 ACSONE SA/NV
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class MisReportInstance(models.Model):

    _inherit = "mis.report.instance"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        string="Operating Unit",
    )


class MisReportInstancePeriod(models.Model):

    _inherit = "mis.report.instance.period"

    operating_unit_ids = fields.Many2many(
        "operating.unit",
        string="Operating Unit",
    )

    def _get_additional_move_line_filter(self):
        aml_domain = super(
            MisReportInstancePeriod, self
        )._get_additional_move_line_filter()
        # we need sudo because, imagine a user having access
        # to operating unit A, viewing a report with 3 columns
        # for OU A, B, C: in columns B and C, self.operating_unit_ids
        # would be empty for him, and the query on a.m.l would be only
        # restricted by the record rules (ie showing move lines
        # for OU A only). So the report would display values
        # for OU A in all 3 columns.
        sudoself = self.sudo()
        if sudoself.report_instance_id.operating_unit_ids:
            aml_domain.append(
                (
                    "operating_unit_id",
                    "in",
                    sudoself.report_instance_id.operating_unit_ids.ids,
                )
            )
        if sudoself.operating_unit_ids:
            aml_domain.append(
                ("operating_unit_id", "in", sudoself.operating_unit_ids.ids)
            )
        return aml_domain
