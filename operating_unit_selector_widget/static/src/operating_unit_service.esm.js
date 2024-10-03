/** @odoo-module **/

import {UPDATE_METHODS} from "@web/core/orm_service";
import {browser} from "@web/core/browser/browser";
import {cookie} from "@web/core/browser/cookie";
import {registry} from "@web/core/registry";
import {session} from "@web/session";

const OUIDS_HASH_SEPARATOR = "-";

function parseOuIds(ou_ids, separator = ",") {
    if (typeof ou_ids === "string") {
        return ou_ids.split(separator).map(Number);
    } else if (typeof ou_ids === "number") {
        return [ou_ids];
    }
    return [];
}

function formatOuIds(ou_ids, separator = ",") {
    return ou_ids.join(separator);
}

function computeActiveOuIds(ou_ids) {
    const {user_ous} = session;
    let activeOuIds = ou_ids || [];
    const availableOusFromSession = user_ous.allowed_ous;
    const notAllowedOus = activeOuIds.filter((id) => !(id in availableOusFromSession));

    if (!activeOuIds.length || notAllowedOus.length) {
        activeOuIds = [user_ous.current_ou];
    }
    return activeOuIds;
}

function getOuIdsFromBrowser(hash) {
    let ou_ids = [];
    if ("ou_ids" in hash) {
        ou_ids = parseOuIds(hash.ou_ids, OUIDS_HASH_SEPARATOR);
    } else if (cookie.get("ou_ids")) {
        ou_ids = parseOuIds(cookie.get("ou_ids"));
    }
    return ou_ids || [];
}

const errorHandlerRegistry = registry.category("error_handlers");
function accessErrorHandler(env, error, originalError) {
    const router = env.services.router;
    const hash = router.current.hash;
    if (!hash._ou_switching) {
        return false;
    }
    if (
        originalError &&
        originalError.exceptionName === "odoo.exceptions.AccessError"
    ) {
        const {model, id, view_type} = hash;
        if (!model || !id || view_type !== "form") {
            return false;
        }
        router.pushState({view_type: undefined});

        browser.setTimeout(() => {
            env.bus.trigger("ROUTE_CHANGE");
        });
        if (error.event) {
            error.event.preventDefault();
        }
        return true;
    }
    return false;
}

export const ouService = {
    dependencies: ["user", "router", "action"],
    start(env, {user, router, action}) {
        errorHandlerRegistry.add("accessErrorHandlerOus", accessErrorHandler);

        const allowedOus = session.user_ous.allowed_ous;
        const activeOuIds = computeActiveOuIds(
            getOuIdsFromBrowser(router.current.hash)
        );

        const ou_ids_hash = formatOuIds(activeOuIds, OUIDS_HASH_SEPARATOR);
        router.replaceState({ou_ids: ou_ids_hash}, {lock: true});
        cookie.set("ou_ids", formatOuIds(activeOuIds));
        user.updateContext({allowed_ou_ids: activeOuIds});

        env.bus.addEventListener("RPC:RESPONSE", (ev) => {
            const {data, error} = ev.detail;
            const {model, method} = data.params;
            if (
                !error &&
                model === "operating.unit" &&
                UPDATE_METHODS.includes(method)
            ) {
                if (!browser.localStorage.getItem("running_tour")) {
                    action.doAction("reload_context");
                }
            }
        });

        return {
            allowedOus,

            get activeOuIds() {
                return activeOuIds.slice();
            },

            get currentOu() {
                return allowedOus[activeOuIds[0]];
            },

            setOus(ouIds) {
                const newOuIds = ouIds.length ? ouIds : [activeOuIds[0]];

                const ou_idsHash = formatOuIds(newOuIds, OUIDS_HASH_SEPARATOR);
                router.pushState({ou_ids: ou_idsHash}, {lock: true});
                router.pushState({_ou_switching: true});
                cookie.set("ou_ids", formatOuIds(newOuIds));
                browser.setTimeout(() => browser.location.reload());
            },
        };
    },
};

registry.category("services").add("operating_unit", ouService);
