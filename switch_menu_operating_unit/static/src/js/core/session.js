odoo.define("switch_menu_operating_unit.Session", function(require) {
    "use strict";

    var core = require("web.core");
    var utils = require("web.utils");

    var OUSession = core.Class.extend({
        setOperatingUnits: function(main_ou_id, ou_ids) {
            var hash = $.bbq.getState();
            hash.ouids = ou_ids
                .sort(function(a, b) {
                    if (a === main_ou_id) {
                        return -1;
                    } else if (b === main_ou_id) {
                        return 1;
                    }
                    return a - b;
                })
                .join(",");
            utils.set_cookie("ouids", hash.ouids || String(main_ou_id));
            $.bbq.pushState({ouids: hash.ouids}, 0);
            location.reload();
        },
    });

    return OUSession;
});
