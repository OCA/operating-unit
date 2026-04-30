# Copyright (C) 2016 ICTSTUDIO (<http://www.ictstudio.eu>).
# Copyright (C) Startx 2021
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.http import Controller, request, route


class WebEasySwitchOperatingUnitController(Controller):
    @route(
        "/web_easy_switch_operating_unit/switch/change_current_operating_unit",
        type="json",
        auth="user",
    )
    def change_current_operating_unit(self, operating_unit_id=False):
        request.env.user.write({"default_operating_unit_id": operating_unit_id})
