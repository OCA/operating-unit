# Copyright 2024 NSI-SA
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models
from odoo.tools import html2plaintext


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    report_header = fields.Html(
        string="Operating Unit Tagline",
        translate=True,
        compute="_compute_report_header",
        store=True,
        readonly=False,
        help="Operating Unit tagline, which is included "
        "in a printed document's header or footer "
        "(depending on the selected layout).",
    )
    report_footer = fields.Html(
        translate=True,
        compute="_compute_report_footer",
        store=True,
        readonly=False,
        help="Footer text displayed at the bottom of all reports.",
    )
    operating_unit_details = fields.Html(
        translate=True,
        compute="_compute_operating_unit_details",
        store=True,
        readonly=False,
        help="Header text displayed at the top of all reports.",
    )
    is_operating_unit_details_empty = fields.Boolean(
        compute="_compute_empty_operating_unit_details"
    )
    partner_image = fields.Image(
        string="Logo",
        compute="_compute_partner_image",
        inverse="_inverse_partner_image",
    )

    @api.depends("partner_id", "partner_id.image_1920")
    def _compute_partner_image(self):
        for operating_unit in self:
            operating_unit.partner_image = operating_unit.partner_id.image_1920

    def _inverse_partner_image(self):
        for operating_unit in self:
            operating_unit.partner_id.image_1920 = operating_unit.partner_image

    @api.depends("company_id")
    def _compute_report_header(self):
        for operating_unit in self:
            operating_unit.report_header = operating_unit.company_id.report_header

    @api.depends("company_id")
    def _compute_report_footer(self):
        for operating_unit in self:
            operating_unit.report_footer = operating_unit.company_id.report_footer

    @api.depends("company_id")
    def _compute_operating_unit_details(self):
        for operating_unit in self:
            operating_unit.operating_unit_details = (
                operating_unit.company_id.company_details
            )

    @api.depends("operating_unit_details")
    def _compute_empty_operating_unit_details(self):
        # In recent change when an html field is
        # empty a <p> balise remains with a <br> in it,
        # but when operating unit details is empty
        # we want to put the info of the operating unit
        for operating_unit in self:
            operating_unit.is_operating_unit_details_empty = not html2plaintext(
                operating_unit.operating_unit_details or ""
            )
