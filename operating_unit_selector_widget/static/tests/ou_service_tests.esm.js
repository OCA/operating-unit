/** @odoo-module **/
/* global QUnit */
/* eslint init-declarations: "warn" */
/* Copyright 2024-TODAY Jérémy Didderen
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */

import {browser} from "@web/core/browser/browser";
import {makeTestEnv} from "@web/../tests/helpers/mock_env";
import {ormService} from "@web/core/orm_service";
import {ouService} from "@operating_unit_selector_widget/operating_unit_service.esm";
import {patchWithCleanup} from "@web/../tests/helpers/utils";
import {registry} from "@web/core/registry";
import {session} from "@web/session";

const serviceRegistry = registry.category("services");

QUnit.module("operating unit service");

QUnit.test("reload webclient when updating a operating.unit", async (assert) => {
    serviceRegistry.add("operating_unit", ouService);
    serviceRegistry.add("orm", ormService);
    serviceRegistry.add("action", {
        start() {
            return {
                doAction(action) {
                    assert.step(action);
                },
            };
        },
    });
    const env = await makeTestEnv();
    assert.verifySteps([]);
    await env.services.orm.read("operating.unit", [32]);
    assert.verifySteps([]);
    await env.services.orm.unlink('operating.unit"', [32]);
    assert.verifySteps(["reload_context"]);
    await env.services.orm.unlink("notaoperatingunit", [32]);
    assert.verifySteps([]);
});

QUnit.test(
    "do not reload webclient when updating a operating.unit, but there is an error",
    async (assert) => {
        serviceRegistry.add("operating_unit", ouService);
        serviceRegistry.add("orm", ormService);
        serviceRegistry.add("action", {
            start() {
                return {
                    doAction(action) {
                        assert.step(action);
                    },
                };
            },
        });
        const env = await makeTestEnv();
        assert.verifySteps([]);
        env.bus.trigger("RPC:RESPONSE", {
            data: {params: {model: "operating.unit", method: "write"}},
            settings: {},
            result: {},
        });
        assert.verifySteps(["reload_context"]);
        env.bus.trigger("RPC:RESPONSE", {
            data: {params: {model: "operating.unit", method: "write"}},
            settings: {},
            error: {},
        });
        assert.verifySteps([]);
    }
);

QUnit.test("extract allowed operating unit ids from url hash", async (assert) => {
    patchWithCleanup(session.user_ous, {
        allowed_companies: {
            1: {id: 1, name: "Main Operating Unit", sequence: 1},
            2: {id: 2, name: "B2B", sequence: 2},
            3: {id: 3, name: "B2C", sequence: 3},
        },
    });

    serviceRegistry.add("operating_unit", ouService);

    Object.assign(browser.location, {hash: "ou_ids=3-1"});
    const env = await makeTestEnv();
    assert.deepEqual(
        Object.values(env.services.ou.allowedOus).map((ou) => ou.id),
        [1, 2, 3]
    );
    assert.deepEqual(env.services.ou.activeOuIds, [3, 1]);
    assert.strictEqual(env.services.ou.currentOu.id, 3);
});
