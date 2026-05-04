/* eslint-disable jsdoc/check-tag-names */
/** @odoo-module **/
/* global window */

import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {session} from "@web/session";
import {useService} from "@web/core/utils/hooks";
import {user} from "@web/core/user";

export class SwitchOperatingUnitMenu extends Component {
    static template = "web_easy_switch_operating_unit.SwitchOperatingUnitMenu";
    static props = {};

    setup() {
        this.orm = useService("orm");
        if (!session.user_operating_units) {
            this.user_operating_units = [];
            this.allowed_operating_unit_ids = [];
            this.current_operating_unit_id = false;
            this.current_operating_unit_name = "No OU";
            return;
        }

        this.user_operating_units =
            session.user_operating_units.allowed_operating_units;
        this.allowed_operating_unit_ids = this.user_operating_units.map((ou) =>
            parseInt(ou[0], 10)
        );
        this.current_operating_unit_id =
            session.user_operating_units.current_operating_unit[0];
        this.current_operating_unit_name =
            session.user_operating_units.current_operating_unit[1];
    }

    async onSwitchOperatingUnitClick(operatingUnitId) {
        await this.orm.write("res.users", [user.userId], {
            default_operating_unit_id: operatingUnitId || false,
        });
        window.location.reload();
    }
}

const systrayItem = {
    Component: SwitchOperatingUnitMenu,
    isDisplayed() {
        return (
            session.user_operating_units &&
            session.user_operating_units.allowed_operating_units.length > 0
        );
    },
};

registry
    .category("systray")
    .add("SwitchOperatingUnitMenu", systrayItem, {sequence: 10});
