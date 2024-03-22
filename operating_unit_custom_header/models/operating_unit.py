from odoo import api, fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    def _get_default_header(self):
        header_id = False
        header = self.env.ref("operating_unit_custom_header.op_header", False)
        if header:
            header_id = header.copy()
        return header_id

    def _get_default_header_xml(self):
        header_id = self.env.ref("operating_unit_custom_header.op_header", False)
        return header_id and header_id.arch_base or False

    def _get_default_footer_xml(self):
        footer_id = self.env.ref("operating_unit_custom_header.op_footer", False)
        return footer_id and footer_id.arch_base or False

    def _get_default_footer(self):
        footer_id = False
        footer = self.env.ref("operating_unit_custom_header.op_footer", False)
        if footer:
            footer_id = footer.copy()
        return footer_id

    footer_view_id = fields.Many2one(
        "ir.ui.view", "Footer Template", default=_get_default_footer
    )

    header_view_id = fields.Many2one(
        "ir.ui.view", "Header Template", default=_get_default_header
    )

    footer = fields.Text(string="Footer", default=_get_default_footer_xml)

    header = fields.Text(string="Header", default=_get_default_header_xml)

    @api.model
    def create(self, values):
        res = super(OperatingUnit, self).create(values)
        res.header_view_id.write(
            {
                "arch_base": res.header,
                "key": "operating_unit_custom_header.header_%s" % res.code,
            }
        )
        res.footer_view_id.write(
            {
                "arch_base": res.footer,
                "key": "operating_unit_custom_header.footer_%s" % res.code,
            }
        )

        return res

    def unlink(self):
        for op in self:
            footer_id = op.footer_view_id
            header_id = op.header_view_id
            super(OperatingUnit, op).unlink()
            footer_id.unlink()
            header_id.unlink()

    def write(self, vals):
        res = super(OperatingUnit, self).write(vals)
        if vals.get("header", False):
            self.header_view_id.arch_base = self.header
        if vals.get("footer", False):
            self.footer_view_id.arch_base = self.footer
        if vals.get("code", False):
            self.header_view_id.key = (
                "operating_unit_custom_header.header_%s" % self.code
            )
            self.footer_view_id.key = (
                "operating_unit_custom_header.footer_%s" % self.code
            )
        return res

    def open_translations_header(self):
        return self.header_view_id.open_translations()

    def open_translations_footer(self):
        return self.footer_view_id.open_translations()
