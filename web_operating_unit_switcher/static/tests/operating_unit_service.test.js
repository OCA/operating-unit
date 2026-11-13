import {describe, expect, test} from "@odoo/hoot";
import {
    getService,
    makeMockEnv,
    patchWithCleanup,
} from "@web/../tests/web_test_helpers";

import {cookie} from "@web/core/browser/cookie";
import {router} from "@web/core/browser/router";
import {session} from "@web/session";

const OU_COOKIE = "ou_id";

const MOCK_OUS = [
    [1, "OU1"],
    [2, "OU2"],
    [3, "OU3"],
];

function setupSession(currentOU = [1, "OU1"], allowedOUs = MOCK_OUS) {
    patchWithCleanup(session, {
        user_operating_units: {
            allowed_operating_units: allowedOUs,
            current_operating_unit: currentOU,
        },
    });
}

describe("OperatingUnitService", () => {
    test("no cookie (first visit) uses user default OU", async () => {
        setupSession();
        await makeMockEnv();
        const ouService = getService("operating_unit");
        expect(ouService.currentOperatingUnitId).toBe(1);
        expect(ouService.allowedOperatingUnits).toEqual(MOCK_OUS);
        expect(cookie.get(OU_COOKIE)).toBe("1");
    });

    test("empty cookie uses no OU (user explicitly cleared)", async () => {
        setupSession();
        cookie.set(OU_COOKIE, "");
        await makeMockEnv();
        const ouService = getService("operating_unit");
        expect(ouService.currentOperatingUnitId).toBe(false);
        expect(ouService.currentOperatingUnit).toEqual([false, false]);
        expect(cookie.get(OU_COOKIE)).toBe("");
    });

    test("change OU to another allowed value", async () => {
        setupSession();
        cookie.set(OU_COOKIE, "2");
        await makeMockEnv();
        const ouService = getService("operating_unit");
        expect(ouService.currentOperatingUnitId).toBe(2);
        expect(ouService.currentOperatingUnit).toEqual([2, "OU2"]);
        expect(cookie.get(OU_COOKIE)).toBe("2");
    });

    test("OU no longer accessible resets to user default", async () => {
        setupSession(
            [1, "OU1"],
            [
                [1, "OU1"],
                [2, "OU2"],
            ]
        );
        cookie.set(OU_COOKIE, "3");
        await makeMockEnv();
        const ouService = getService("operating_unit");
        expect(ouService.currentOperatingUnitId).toBe(1);
        expect(ouService.currentOperatingUnit).toEqual([1, "OU1"]);
        expect(cookie.get(OU_COOKIE)).toBe("1");
    });

    test("switch to another OU reloads the page", async () => {
        setupSession();
        await makeMockEnv();
        patchWithCleanup(router, {
            pushState(state, options) {
                expect.step(options?.reload ? "reload" : "navigate");
            },
        });
        const ouService = getService("operating_unit");
        ouService.setOperatingUnit(3);
        expect(cookie.get(OU_COOKIE)).toBe("3");
        expect.verifySteps(["reload"]);
    });

    test("clear OU selection reloads the page", async () => {
        setupSession();
        cookie.set(OU_COOKIE, "2");
        await makeMockEnv();
        patchWithCleanup(router, {
            pushState(state, options) {
                expect.step(options?.reload ? "reload" : "navigate");
            },
        });
        const ouService = getService("operating_unit");
        ouService.setOperatingUnit(false);
        expect(cookie.get(OU_COOKIE)).toBe("");
        expect.verifySteps(["reload"]);
    });

    test("user with no operating units gets no switcher", async () => {
        patchWithCleanup(session, {user_operating_units: null});
        await makeMockEnv();
        expect(getService("operating_unit")).toEqual({});
    });
});
