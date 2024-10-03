/** @odoo-module **/
import {Component, useChildSubEnv, useState} from "@odoo/owl";
import {Dropdown} from "@web/core/dropdown/dropdown";
import {DropdownItem} from "@web/core/dropdown/dropdown_item";
import {debounce} from "@web/core/utils/timing";
import {registry} from "@web/core/registry";
import {useService} from "@web/core/utils/hooks";

export class OuSelector {
    constructor(ouService, toggleDelay) {
        this.ouService = ouService;
        this.selectedOusIds = ouService.activeOuIds.slice();

        this._debouncedApply = debounce(() => this._apply(), toggleDelay);
    }

    isOuSelected(ouId) {
        return this.selectedOusIds.includes(ouId);
    }

    switchOu(mode, ouId) {
        if (mode === "toggle") {
            if (this.selectedOusIds.includes(ouId)) {
                this._deselectOu(ouId);
            } else {
                this._selectOu(ouId);
            }
            this._debouncedApply();
        } else if (mode === "loginto") {
            this._selectOu(ouId, true);
            this._apply();
        }
    }

    _selectOu(ouId, unshift = false) {
        if (!this.selectedOusIds.includes(ouId)) {
            if (unshift) {
                this.selectedOusIds.unshift(ouId);
            } else {
                this.selectedOusIds.push(ouId);
            }
        } else if (unshift) {
            const index = this.selectedOusIds.findIndex((ou) => ou === ouId);
            this.selectedOusIds.splice(index, 1);
            this.selectedOusIds.unshift(ouId);
        }
    }

    _deselectOu(ouId) {
        if (this.selectedOusIds.includes(ouId)) {
            this.selectedOusIds.splice(this.selectedOusIds.indexOf(ouId), 1);
        }
    }

    _apply() {
        this.ouService.setOus(this.selectedOusIds, false);
    }
}

export class SwitchOuItem extends Component {
    static template = "operating_unit_selector_widget.SwitchOuItem";
    static components = {DropdownItem, SwitchOuItem};
    static props = {
        ou: {},
        level: {type: Number},
    };

    setup() {
        this.ouService = useService("operating_unit");
        this.ouSelector = useState(this.env.ouSelector);
    }

    get isOuSelected() {
        return this.ouSelector.isOuSelected(this.props.ou.id);
    }

    get isOuAllowed() {
        return this.props.ou.id in this.ouService.allowedOus;
    }

    get isCurrent() {
        return this.props.ou.id === this.ouService.currentOu.id;
    }

    logIntoOu() {
        if (this.isOuAllowed) {
            this.ouSelector.switchOu("loginto", this.props.ou.id);
        }
    }

    toggleOu() {
        if (this.isOuAllowed) {
            this.ouSelector.switchOu("toggle", this.props.ou.id);
        }
    }
}

export class SwitchOuMenu extends Component {
    static template = "operating_unit_selector_widget.SwitchOuMenu";
    static components = {Dropdown, DropdownItem, SwitchOuItem};
    static props = {};
    static toggleDelay = 1000;
    static OuSelector = OuSelector;

    setup() {
        this.ouService = useService("operating_unit");

        this.ouSelector = useState(
            new this.constructor.OuSelector(
                this.ouService,
                this.constructor.toggleDelay
            )
        );
        useChildSubEnv({ouSelector: this.ouSelector});
    }
}

export const systrayItem = {
    Component: SwitchOuMenu,
    isDisplayed(env) {
        const {allowedOus} = env.services.operating_unit;
        return Object.keys(allowedOus).length > 1;
    },
};

registry.category("systray").add("SwitchOuMenu", systrayItem, {sequence: 1});
