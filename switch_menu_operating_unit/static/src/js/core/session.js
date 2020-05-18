odoo.define("switch_menu_operating_unit.Session", function (require) {
"use strict" ;

var ajax = require('web.ajax');
var concurrency = require('web.concurrency');
var core = require('web.core');
var local_storage = require('web.local_storage');
var mixins = require('web.mixins');
var utils = require('web.utils');
var session = require("web.session");
var _t = core._t;
var qweb = core.qweb;

var OUSession = core.Class.extend(Session, {
    setOperatingUnits: function (main_ou_id, ou_ids) {
        var hash = $.bbq.getState();
        hash.ouids = ou_ids.sort(function (a, b) {
            if (a === main_ou_id) {
                return -1;
            } else if (b === main_ou_id) {
                return 1;
            } else {
                return a - b;
            }
        }).join(',');
        utils.set_cookie(ouids, hash.ouids || String(main_ou_id));
        $.bbq.pushState({'ouids': hash.ouids}, 0);
        location.reload()
    }
});

return OUSession
});
