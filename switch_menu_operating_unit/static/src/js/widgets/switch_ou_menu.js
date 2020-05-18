odoo.define("switch_menu_operating_unit.SwitchOperatingMenu", function(require) {
    "use strict";

    /**
     * When Odoo add mulit-companies support we need
     * a dropdown to work with operating_unit as same
     */

    var config = require("web.config");
    var session = require("web.session");
    var SystrayMenu = require("web.SystrayMenu");
    var Widget = require("web.Widget");

    var SwitchOperatingMenu = Widget.extend({
        template: "SwitchOperatingMenu",
        events: {
            "click .dropdown-item[data-menu] div.log_into":
                "_onSwitchOperatingUnitClick",
            "keydown .dropdown-item[data-menu] div.log_into":
                "_onSwitchOperatingUnitClick",
            "click .dropdown-item[data-menu] div.toggle_operating_unit":
                "_onToggleOperatingUnitClick",
            "keydown .dropdown-item[data-menu] div.toggle_operating_unit":
                "_onToggleOperatingUnitClick",
        },
        /**
         * @override
         */
        init: function() {
            this._super.apply(this, arguments);
            this.isMobile = config.device.isMobile;
            this._onSwitchOperatingUnitClick = _.debounce(
                this._onSwitchOperatingUnitClick,
                1500,
                true
            );
        },

        /**
         * @override
         */
        willStart: function() {
            var self = this;
            this.allowed_operating_unit_ids = String(
                session.user_context.allowed_operating_unit_ids
            )
                .split(",")
                .map(function(id) {
                    return parseInt(id);
                });
            this.user_operating_units =
                session.user_operating_units.allowed_operating_units;
            this.current_operating_unit = this.allowed_operating_unit_ids[0];
            this.current_operating_unit_name = _.find(
                session.user_operating_units.allowed_operating_units,
                function(operating_unit) {
                    return operating_unit[0] === self.current_operating_unit;
                }
            )[1];

            return this._super.apply(this, arguments);
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onSwitchOperatingUnitClick: function(ev) {
            if (
                ev.type === "key_down" &&
                ev.which !== $.ui.keyCode.ENTER &&
                ev.which !== $.ui.keyCode.SPACE
            ) {
                return;
            }
            ev.preventDefault();
            ev.stopPropagation();
            var dropdownItem = $(ev.currentTarget).parent();
            var dropdownMenu = dropdownItem.parent();
            var operatingUnitID = dropdownItem.data("operating_unit-id");
            var allowed_operating_unit_ids = this.allowed_operating_unit_ids;
            if (dropdownItem.find(".fa-square-o").length) {
                // 1 enabled operating_unit: Stay in single operating_unit mode
                if (this.allowed_operating_unit_ids.length === 1) {
                    if (this.isMobile) {
                        dropdownMenu = dropdownMenu.parent();
                    }
                    dropdownMenu
                        .find(".fa-check-square")
                        .removeClass("fa-check-square")
                        .addClass("fa-square-o");
                    dropdownItem
                        .find(".fa-square-o")
                        .removeClass("fa-square-o")
                        .addClass("fa-check-square");
                    allowed_operating_unit_ids = [operatingUnitID];
                } else {
                    allowed_operating_unit_ids.push(operatingUnitID);
                    dropdownItem
                        .find(".fa-square-o")
                        .removeClass("fa-square-o")
                        .addClass("fa-check-square");
                }
            }
            $(ev.currentTarget).attr("aria-pressed", "true");
            session.setOperatingUnits(operatingUnitID, allowed_operating_unit_ids);
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onToggleOperatingUnitClick: function(ev) {
            if (
                ev.type === "keydown" &&
                ev.which !== $.ui.keyCode.ENTER &&
                ev.which !== $.ui.keyCode.SPACE
            ) {
                return;
            }
            ev.preventDefault();
            ev.stopPropagation();
            var dropdownItem = $(ev.currentTarget).parent();
            var operatingUnitID = dropdownItem.data("operating_unit-id");
            var allowed_operating_unit_ids = this.allowed_operating_unit_ids;
            var current_operating_unit_id = allowed_operating_unit_ids[0];
            if (dropdownItem.find(".fa-square-o").length) {
                allowed_operating_unit_ids.push(operatingUnitID);
                dropdownItem
                    .find(".fa-square-o")
                    .removeClass("fa-square-o")
                    .addClass("fa-check-square");
                $(ev.currentTarget).attr("aria-checked", "true");
            } else {
                allowed_operating_unit_ids.splice(
                    allowed_operating_unit_ids.indexOf(operatingUnitID),
                    1
                );
                dropdownItem
                    .find(".fa-check-square")
                    .addClass("fa-square-o")
                    .removeClass("fa-check-square");
                $(ev.currentTarget).attr("aria-checked", "false");
            }
            session.setOperatingUnits(
                current_operating_unit_id,
                allowed_operating_unit_ids
            );
        },
    });

    if (session.display_switch_operating_unit_menu) {
        SystrayMenu.Items.push(SwitchOperatingMenu);
    }

    return SwitchOperatingMenu;
});
