# Copyright 2024-TODAY Jérémy Didderen
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models


class Http(models.AbstractModel):
    _inherit = "ir.http"

    def session_info(self):
        session_info = super().session_info()
        user = self.env.user
        is_internal_user = user.has_group("base.group_user")
        if is_internal_user:
            session_info.update(
                {
                    "user_ous": {
                        "current_ou": user.default_operating_unit_id.id,
                        "allowed_ous": {
                            ou.id: {
                                "id": ou.id,
                                "name": ou.name,
                                "sequence": ou.sequence,
                            }
                            for ou in user.operating_unit_ids
                        },
                    },
                }
            )
        return session_info
