/* eslint-disable jsdoc/check-tag-names */
/** @odoo-module **/

import {Component} from "@odoo/owl";
import {registry} from "@web/core/registry";
import {session} from "@web/session";
import {useService} from "@web/core/utils/hooks";

/**
 * Systray component to switch the current operating unit.
 * Uses the operating_unit service which stores the selection in a cookie,
 * enabling a different OU per browser tab.
 */
export class SwitchOperatingUnitMenu extends Component {
    static template = "web_easy_switch_operating_unit.SwitchOperatingUnitMenu";
    static props = {};

    setup() {
        this.ouService = useService("operating_unit");
        this.user_operating_units = this.ouService.allowedOperatingUnits || [];
        this.allowed_operating_unit_ids = this.user_operating_units.map((ou) => ou[0]);
        this.current_operating_unit_id = this.ouService.currentOperatingUnitId || false;
        const current = this.ouService.currentOperatingUnit;
        this.current_operating_unit_name = current[0] ? current[1] : "No OU";
    }

    onSwitchOperatingUnitClick(operatingUnitId) {
        this.ouService.setOperatingUnit(operatingUnitId || false);
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
