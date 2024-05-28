/** @odoo-module **/

import {AnalyticDistribution} from "@analytic/components/analytic_distribution/analytic_distribution";
import {patch} from "@web/core/utils/patch";

patch(AnalyticDistribution.prototype, {
    recordProps(line) {
        var res = super.recordProps(line);
        if ("fields" in res) {
            for (const [key, value] of Object.entries(res.fields)) {
                if (key.startsWith("x_plan") && "domain" in value) {
                    if (
                        "operating_unit_id" in this.props.record.data &&
                        this.props.record.data.operating_unit_id
                    ) {
                        res.fields[key].domain.push(
                            "|",
                            [
                                "operating_unit_ids",
                                "in",
                                this.props.record.data.operating_unit_id[0],
                            ],
                            ["operating_unit_ids", "=", false]
                        );
                    }
                }
            }
        }
        return res;
    },
});
