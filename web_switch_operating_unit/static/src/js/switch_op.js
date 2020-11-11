odoo.define("web_switch_operating_unit.SwitchOPs", function (require) {
    "use strict";

    var config = require("web.config");
    var core = require("web.core");
    var session = require("web.session");
    var SystrayMenu = require("web.SystrayMenu");
    var Widget = require("web.Widget");

    var _t = core._t;

    var SwitchOPs = Widget.extend({
        template: "SwitchOPs",
        events: {
            "click .dropdown-item[data-menu]": "_onClick",
        },

        /**
     * @override
     */
        init: function () {
            this._super.apply(this, arguments);
            this.isMobile = config.device.isMobile;
            this._onClick = _.debounce(this._onClick, 1500, true);
        },

        /**
     * @override
     */
        willStart: function () {
            return session.user_ops ? this._super() : $.Deferred().reject();
        },

        /**
     * @override
     */
        start: function () {
            var OpList = "";
            if (this.isMobile) {
                OpList = "<li class=\"bg-info\">" +
                _t("Tap on the list to change Operating Unit") + "</li>";
            } else {
                this.$(".oe_topbar_name").text(session.user_ops.current_op[1]);
            }
            _.each(session.user_ops.allowed_ops, function (op) {
                var a = "";
                var isCurrentOp = op[0] === session.user_ops.current_op[0];
                if (isCurrentOp) {
                    a = "<i class=\"fa fa-check mr8\"></i>";
                } else {
                    a = "<span style=\"margin-right: 24px;\"/>";
                }
                OpList += "<a role=\"menuitemradio\" aria-checked=\"" +
                isCurrentOp +"\" href=\"#\" class=\"dropdown-item\""+
                "data-menu=\"op\" data-op-id=\""+
                op[0] + "\">" + a + op[1] + "</a>";
            });
            this.$(".dropdown-menu").html(OpList);
            return this._super();
        },

        /**
     * @private
     * @param {MouseEvent} ev
     */
        _onClick: function (ev) {
            var opID = $(ev.currentTarget).data("op-id");
            this._rpc({
                model: "res.users",
                method: "write",
                args: [[session.uid], {"default_operating_unit_id": opID}],
            })
                .then(function () {
                    location.reload();
                });

        },
    });
    SystrayMenu.Items.push(SwitchOPs);
    return SwitchOPs;
});
