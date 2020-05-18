/* Copyright 2020 Antoni Romera
 * License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl). */
/* eslint-disable */
/*
The version of eslint no support spread operator
{
    session: {
        ...params.session,
        setOperatingUnits: function(mainOperatingUnitId, OperatingUnitIds) {
            assert.equal(
                mainOperatingUnitId,
                params.assertMainOperatingUnit[0],
                params.assertMainOperatingUnit[1]
            );
            assert.equal(
                _.intersection(OperatingUnitIds, params.asserOperatingUnits[0])
                    .length,
                params.asserOperatingUnits[0].length,
                params.asserOperatingUnits[1]
            );
        },
    },
}
*/
odoo.define("switch_menu_operating_unit.SwitchOperatingUnitMenu_tests", function(
    require
) {
    "use strict";

    var SwitchOperatingUnitMenu = require("switch_menu_operating_unit.SwitchOperatingUnitMenu");
    var testUtils = require("web.test_utils");

    async function createSwitchOperatingUnitMenu(params) {
        params = params || {};
        var target = params.debug ? document.body : $("#qunit-fixture");
        var menu = new SwitchOperatingUnitMenu();
        testUtils.mock.addMockEnvironment(menu, params);
        await menu.appendTo(target);
        return menu;
    }

    async function initMockOperatingUnitMenu(assert, params) {
        var menu = await createSwitchOperatingUnitMenu({
            session: Object.assign({}, params.session, {
                setOperatingUnits: function(mainOperatingUnitId, OperatingUnitIds) {
                    assert.equal(
                        mainOperatingUnitId,
                        params.assertMainOperatingUnit[0],
                        params.assertMainOperatingUnit[1]
                    );
                    assert.equal(
                        _.intersection(OperatingUnitIds, params.asserOperatingUnits[0])
                            .length,
                        params.asserOperatingUnits[0].length,
                        params.asserOperatingUnits[1]
                    );
                },
            }),
        });
        await testUtils.dom.click(menu.$(".dropdown-toggle")); // Open OperatingUnit switcher dropdown
        return menu;
    }

    async function testSwitchOperatingUnit(assert, params) {
        assert.expect(2);
        var menu = await initMockOperatingUnitMenu(assert, params);
        await testUtils.dom.click(
            menu.$(`div[data-operating_unit-id=${params.operating_unit}] div.log_into`)
        );
        menu.destroy();
    }

    async function testToggleOperatingUnit(assert, params) {
        assert.expect(2);
        var menu = await initMockOperatingUnitMenu(assert, params);
        await testUtils.dom.click(
            menu.$(
                `div[data-operating_unit-id=${params.operating_unit}] div.toggle_operating_unit`
            )
        );
        menu.destroy();
    }

    QUnit.module(
        "widgets",
        {
            beforeEach: async function() {
                (this.session_mock_mutil = {
                    user_operating_units: {
                        current_operating_unit: ["1", "Operating Unit 1"],
                        allowed_operating_units: [
                            ["1", "Operating Unit 1"],
                            ["2", "Operating Unit 2"],
                            ["3", "Operating Unit 3"],
                        ],
                    },
                    user_context: {allowed_operating_unit_ids: [1, 3]},
                }),
                    (this.session_mock_single = {
                        user_operating_units: {
                            current_operating_unit: ["1", "Operating Unit 1"],
                            allowed_operating_units: [
                                ["1", "Operating Unit 1"],
                                ["2", "Operating Unit 2"],
                                ["3", "Operating Unit 3"],
                            ],
                        },
                        user_context: {allowed_operating_unit_ids: [1]},
                    });
            },
        },
        function() {
            QUnit.module("SwitchOperatingUnitMenu", {}, function() {
                QUnit.test("OperatingUnit switcher basic rendering", async function(
                    assert
                ) {
                    assert.expect(6);
                    var menu = await createSwitchOperatingUnitMenu({
                        session: this.session_mock_multi,
                    });
                    assert.equal(
                        menu.$(".operating_unit_label:contains(Operating Unit 1)")
                            .length,
                        1,
                        "it should display Operating Unit 1"
                    );
                    assert.equal(
                        menu.$(".operating_unit_label:contains(Operating Unit 2)")
                            .length,
                        1,
                        "it should display Operating Unit 2"
                    );
                    assert.equal(
                        menu.$(".operating_unit_label:contains(Operating Unit 3)")
                            .length,
                        1,
                        "it should display Operating Unit 3"
                    );

                    assert.equal(
                        menu.$("div[data-operating_unit-id=1] .fa-check-square").length,
                        1,
                        "Operating Unit 1 should be checked"
                    );
                    assert.equal(
                        menu.$("div[data-operating_unit-id=2] .fa-square-o").length,
                        1,
                        "Operating Unit 2 should not be checked"
                    );
                    assert.equal(
                        menu.$("div[data-operating_unit-id=3] .fa-check-square").length,
                        1,
                        "Operating Unit 3 should be checked"
                    );
                    menu.destroy();
                });
            });

            QUnit.module("SwitchOperatingUnitMenu", {}, function() {
                QUnit.test(
                    "Toggle new operating unit in multiple operating unit mode",
                    async function(assert) {
                        /**
                         *          [x] **Operating Unit 1**          [x] **Operating Unit 1**
                         *  toggle->[ ] Operating Unit 2     ====>    [x] Operating Unit 2
                         *          [x] Operating Unit 3              [x] Operating Unit 3
                         */
                        await testToggleOperatingUnit(assert, {
                            operating_unit: 2,
                            session: this.session_mock_multi,
                            assertMainOperatingUnit: [
                                1,
                                "Main operating unit should not have changed",
                            ],
                            asserOperatingUnits: [
                                [1, 2, 3],
                                "All operating units should be activated",
                            ],
                        });
                    }
                );

                QUnit.test(
                    "Toggle active operating unit in mutliple operating unit mode",
                    async function(assert) {
                        /**
                         *          [x] **Operating Unit 1**          [x] **Operating Unit 1**
                         *          [ ] Operating Unit 2     ====>    [ ] Operating Unit 2
                         *  toggle->[x] Operating Unit 3              [ ] Operating Unit 3
                         */
                        await testToggleOperatingUnit(assert, {
                            operating_unit: 3,
                            session: this.session_mock_multi,
                            assertMainOperatingUnit: [
                                1,
                                "Main operating unit should not have changed",
                            ],
                            asserOperatingUnits: [
                                [1],
                                "Operating unit 3 should be unactivated",
                            ],
                        });
                    }
                );

                QUnit.test(
                    "Switch main operating unit in mutliple operating unit mode",
                    async function(assert) {
                        /**
                         *          [x] **Operating Unit 1**          [x] Operating Unit 1
                         *          [ ] Operating Unit 2     ====>    [ ] Operating Unit 2
                         *  switch->[x] Operating Unit 3              [x] **Operating Unit 3**
                         */
                        await testSwitchOperatingUnit(assert, {
                            operating_unit: 3,
                            session: this.session_mock_multi,
                            assertMainOperatingUnit: [
                                3,
                                "Main operating unit should switch to Operating Unit 3",
                            ],
                            asserOperatingUnits: [
                                [1, 3],
                                "Operating units 1 and 3 should still be active",
                            ],
                        });
                    }
                );

                QUnit.test(
                    "Switch new operating unit in mutliple operating unit mode",
                    async function(assert) {
                        /**
                         *          [x] **Operating Unit 1**          [x] Operating Unit 1
                         *  switch->[ ] Operating Unit 2     ====>    [x] **Operating Unit 2**
                         *          [x] Operating Unit 3              [x] Operating Unit 3
                         */
                        await testSwitchOperatingUnit(assert, {
                            operating_unit: 2,
                            session: this.session_mock_multi,
                            assertMainOperatingUnit: [
                                2,
                                "Operating unit 2 should become the main operating unit",
                            ],
                            asserOperatingUnits: [
                                [1, 2, 3],
                                "Operating units 1 and 3 should still be active",
                            ],
                        });
                    }
                );

                QUnit.test(
                    "Switch main operating unit in single operating unit mode",
                    async function(assert) {
                        /**
                         *          [x] **Operating Unit 1**          [ ] Operating Unit 1
                         *          [ ] Operating Unit 2     ====>    [ ] Operating Unit 2
                         *  switch->[ ] Operating Unit 3              [x] **Operating Unit 3**
                         */
                        await testSwitchOperatingUnit(assert, {
                            operating_unit: 3,
                            session: this.session_mock_single,
                            assertMainOperatingUnit: [
                                3,
                                "Main operating unit should switch to Operating Unit 3",
                            ],
                            asserOperatingUnits: [
                                [3],
                                "Operating unit 1 should no longer be active",
                            ],
                        });
                    }
                );

                QUnit.test("Toggle new company in single company mode", async function(
                    assert
                ) {
                    /**
                     *          [x] **Operating Unit 1**          [ ] **Operating Unit 1**
                     *          [ ] Operating Unit 2     ====>    [ ] Operating Unit 2
                     *  toggle->[ ] Operating Unit 3              [x] Operating Unit 3
                     */
                    await testToggleOperatingUnit(assert, {
                        operating_unit: 3,
                        session: this.session_mock_single,
                        assertMainOperatingUnit: [
                            1,
                            "Operating Unit 1 should still be the main operating unit",
                        ],
                        asserOperatingUnits: [
                            [1, 3],
                            "Operating unit 3 should be activated",
                        ],
                    });
                });
            });
        }
    );
});
