/* eslint-disable jsdoc/check-tag-names */
/** @odoo-module **/

import {cookie} from "@web/core/browser/cookie";
import {registry} from "@web/core/registry";
import {router} from "@web/core/browser/router";
import {session} from "@web/session";
import {user} from "@web/core/user";

const OU_COOKIE = "ou_id";

export const operatingUnitService = {
    start() {
        const userOUs = session.user_operating_units;
        if (!userOUs) {
            return {};
        }

        const allowedOUs = userOUs.allowed_operating_units;
        const allowedIds = allowedOUs.map((ou) => ou[0]);
        const defaultOUId = userOUs.current_operating_unit[0];

        // No cookie (first visit) vs empty cookie (user cleared OU)
        const cookieValue = cookie.get(OU_COOKIE);
        let currentOUId = false;
        if (cookieValue === undefined) {
            // First visit — use the user's DB default
            currentOUId = defaultOUId;
        } else if (cookieValue === "") {
            // User explicitly cleared the OU
            currentOUId = false;
        } else {
            currentOUId = parseInt(cookieValue, 10);
            if (!allowedIds.includes(currentOUId)) {
                // Cookie references an OU the user no longer has access to
                currentOUId = defaultOUId;
            }
        }

        cookie.set(OU_COOKIE, currentOUId || "");
        user.updateContext({current_operating_unit_id: currentOUId || false});

        return {
            get currentOperatingUnitId() {
                return currentOUId;
            },
            get currentOperatingUnit() {
                return allowedOUs.find((ou) => ou[0] === currentOUId) || [false, false];
            },
            get allowedOperatingUnits() {
                return allowedOUs;
            },
            setOperatingUnit(ouId) {
                cookie.set(OU_COOKIE, ouId || "");
                user.updateContext({current_operating_unit_id: ouId || false});
                router.pushState({}, {reload: true});
            },
        };
    },
};

registry.category("services").add("operating_unit", operatingUnitService);
