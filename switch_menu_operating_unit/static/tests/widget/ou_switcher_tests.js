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
        });
        await testUtils.dom.click(menu.$(".dropdown-toggle")); // open OperatingUnit switcher dropdown
        return menu;
    }

    async function testSwitchOperatingUnit(assert, params) {
        assert.expect(2);
        var menu = await initMockOperatingUnitMenu(assert, params);
        await testUtils.dom.click(
            menu.$(`div[data-OperatingUnit-id=${params.OperatingUnit}] div.log_into`)
        );
        menu.destroy();
    }
});
