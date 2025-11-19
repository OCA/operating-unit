import {AnalyticDistribution} from "@analytic/components/analytic_distribution/analytic_distribution";
import {patch} from "@web/core/utils/patch";

patch(AnalyticDistribution.prototype, {
    recordProps(line) {
        var res = super.recordProps(line);
        if ("fields" in res) {
            for (const [key, value] of Object.entries(res.fields)) {
                if (key.startsWith("x_plan") && "domain" in value) {
                    // NB: The JS part here is **generic** and doesn't work alone.
                    // The `operating_unit_id` field is provided by the models that use an analytic distribution.
                    // For example,
                    // the `account.move.line` will have the field (defined in `account_operating_unit` module),
                    // and then, this JS will be applied in that context.
                    if (
                        "operating_unit_id" in this.props.record.data &&
                        this.props.record.data.operating_unit_id
                    ) {
                        res.fields[key].domain.push(
                            "|",
                            [
                                "operating_unit_ids",
                                "in",
                                this.props.record.data.operating_unit_id.id,
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
