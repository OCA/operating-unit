# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        session_info = super(Http, self).session_info()

        user = request.env.user

        session_info["user_context"].update(
            {"allowed_operating_unit_ids": user.operating_unit_ids.ids}
        )

        session_info.update(
            {
                "user_operating_units": {
                    "current_operating_unit": (
                        user.default_operating_unit_id.id,
                        user.default_operating_unit_id.name,
                    ),
                    "allowed_operating_units": [
                        (ou.id, ou.name) for ou in user.operating_unit_ids
                    ],
                },
                "display_switch_ou_menu": len(user.operating_unit_ids) > 1,
                # user.has_group('base.group_multi_company') \
                # and len(user.company_ids) > 1,
            }
        )

        return session_info
