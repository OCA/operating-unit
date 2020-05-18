odoo.define("switch_menu_operating_unit.SwitchOuMenu", function(require) {
    "use strict";

    /**
     * When Odoo add mulit-companies support we need
     * a dropdown to work with OU as same
     */

    var config = require("web.config");
    var session = require("web.session");
    var SystrayMenu = require("web.SystrayMenu");
    var Widget = require("web.Widget");

    var SwitchOuMenu = Widget.extend({
        template: "SwitchOuMenu",
        events: {
            "click .dropdown-item[data-menu] div.log_into": "_onSwitchOuClick",
            "keydown .dropdown-item[data-menu] div.log_into": "_onSwitchOuClick",
            "click .dropdown-item[data-menu] div.toggle_ou": "_onToggleOuClick",
            "keydown .dropdown-item[data-menu] div.toggle_ou": "_onToggleOuClick",
        },
        /**
         * @override
         */
        init: function() {
            this._super.apply(this, arguments);
            this.isMobile = config.device.isMobile;
            this._onSwitchOuClick = _.debounce(this._onSwitchOuClick, 1500, true);
        },

        /**
         * @override
         */
        willStart: function() {
            var self = this;
            this.allowed_ou_ids = String(
                session.user_context.allowed_operating_unit_ids
            )
                .split(",")
                .map(function(id) {
                    return parseInt(id);
                });
            this.user_operating_units =
                session.user_operating_units.allowed_operating_units;
            this.current_ou = this.allowed_ou_ids[0];
            this.current_ou_name = _.find(
                session.user_operating_units.allowed_operating_units,
                function(ou) {
                    return ou[0] === self.current_ou;
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
        _onSwitchOuClick: function(ev) {
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
            var ouID = dropdownItem.data("ou-id");
            var allowed_ou_ids = this.allowed_ou_ids;
            if (dropdownItem.find(".fa-square-o").length) {
                // 1 enabled ou: Stay in single ou mode
                if (this.allowed_ou_ids.length === 1) {
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
                    allowed_ou_ids = [ouID];
                } else {
                    allowed_ou_ids.push(ouID);
                    dropdownItem
                        .find(".fa-square-o")
                        .removeClass("fa-square-o")
                        .addClass("fa-check-square");
                }
            }
            $(ev.currentTarget).attr("aria-pressed", "true");
            session.setOperatingUnits(ouID, allowed_ou_ids);
        },

        // --------------------------------------------------------------------------
        // Handlers
        // --------------------------------------------------------------------------

        /**
         * @private
         * @param {MouseEvent|KeyEvent} ev
         */
        _onToggleOuClick: function(ev) {
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
            var ouID = dropdownItem.data("ou-id");
            var allowed_ou_ids = this.allowed_ou_ids;
            var current_ou_id = allowed_ou_ids[0];
            if (dropdownItem.find(".fa-square-o").length) {
                allowed_ou_ids.push(ouID);
                dropdownItem
                    .find(".fa-square-o")
                    .removeClass("fa-square-o")
                    .addClass("fa-check-square");
                $(ev.currentTarget).attr("aria-checked", "true");
            } else {
                allowed_ou_ids.splice(allowed_ou_ids.indexOf(ouID), 1);
                dropdownItem
                    .find(".fa-check-square")
                    .addClass("fa-square-o")
                    .removeClass("fa-check-square");
                $(ev.currentTarget).attr("aria-checked", "false");
            }
            session.setOperatingUnits(current_ou_id, allowed_ou_ids);
        },
    });

    if (session.display_switch_ou_menu) {
        SystrayMenu.Items.push(SwitchOuMenu);
    }

    return SwitchOuMenu;
});
