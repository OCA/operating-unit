from . import models
from odoo import api, SUPERUSER_ID


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    op_ids = env["operating.unit"].search([])
    for op in op_ids:
        op.footer_view_id = op._get_default_footer()
        op.header_view_id = op._get_default_header()
        op.footer = op._get_default_footer_xml()
        op.header = op._get_default_header_xml()
        op.header_view_id.write(
            {
                "arch_base": op.header,
                "key": "operating_unit_custom_header.header_%s" % op.code,
            }
        )
        op.footer_view_id.write(
            {
                "arch_base": op.footer,
                "key": "operating_unit_custom_header.footer_%s" % op.code,
            }
        )
