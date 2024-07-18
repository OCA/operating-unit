/** @odoo-module **/

import {AnalyticDistribution} from "@analytic/components/analytic_distribution/analytic_distribution";
import {patch} from "@web/core/utils/patch";

patch(AnalyticDistribution.prototype, "analytic_operating_unit", {
    analyticAccountDomain(groupId = null) {
        var domain = this._super(groupId);
        if (this.props.record.data.operating_unit_id) {
            domain.push(
                "|",
                [
                    "operating_unit_ids",
                    "=",
                    this.props.record.data.operating_unit_id[0],
                ],
                ["operating_unit_ids", "=", false]
            );
        }
        return domain;
    },
});
