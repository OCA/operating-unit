odoo.define('web_easy_switch_operating_unit.SwitchOperatingUnitMenu', function(require) {
"use strict";

var config = require('web.config');
var session = require('web.session');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var SwitchOperatingUnitMenu = Widget.extend({
    template: 'SwitchOperatingUnitMenu',
    events: {
        'click .dropdown-item[data-menu] div.log_into': '_onSwitchOperatingUnitClick',
        'keydown .dropdown-item[data-menu] div.log_into': '_onSwitchOperatingUnitClick',
    },
    /**
     * @override
     */
    init: function () {
        this._super.apply(this, arguments);
        this.isMobile = config.device.isMobile;
        this._onSwitchOperatingUnitClick = _.debounce(this._onSwitchOperatingUnitClick, 1500, true);
    },

    /**
     * @override
     */
    willStart: function () {
        this.user_operating_units = session.user_operating_units.allowed_operating_units;
        this.allowed_operating_unit_ids = this.user_operating_units
                                          .map(function (ou) {return parseInt(ou[0], 10);});
        this.current_operating_unit_id = session.user_operating_units.current_operating_unit[0];
        this.current_operating_unit_name = session.user_operating_units.current_operating_unit[1];

        return this._super.apply(this, arguments);
    },

    /**
     * @private
     * @param {MouseEvent|KeyEvent} ev
     */
    _onSwitchOperatingUnitClick: function (ev) {
        if (ev.type === 'keydown' && ev.which !== $.ui.keyCode.ENTER && ev.which !== $.ui.keyCode.SPACE) {
            return;
        }
        ev.preventDefault();
        ev.stopPropagation();
        var dropdownItem = $(ev.currentTarget).parent();
        var operating_unit_id = dropdownItem.data('operating-unit-id');
        $(ev.currentTarget).attr('aria-pressed', 'true');

        this._rpc({
            'route': '/web_easy_switch_operating_unit/switch/change_current_operating_unit',
            'params': {
                'operating_unit_id': operating_unit_id,
            }
        }).then(
            function () {
              window.location.reload();
            }
        );
    }
});


SystrayMenu.Items.push(SwitchOperatingUnitMenu);

return SwitchOperatingUnitMenu;
});
