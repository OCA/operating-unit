# © 2020 Vishnu Vanneri
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import models
from odoo.http import request


class Http(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        res = super(Http, self).session_info()
        user = request.env.user
        display_switch_op_menu = len(user.operating_unit_ids) > 1
        res.update({
            "user_ops":
                {
                    "current_op": (user.default_operating_unit_id.id,
                                   user.default_operating_unit_id.name),
                    "allowed_ops": [(comp.id, comp.name) for comp in
                                    user.operating_unit_ids]
                } if display_switch_op_menu else False,
        })

        return res
