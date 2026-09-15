import {Field} from "@web/views/fields/field";
import {patch} from "@web/core/utils/patch";

patch(Field.prototype, {
    get fieldComponentProps() {
        const props = super.fieldComponentProps;

        if (!("context" in props)) {
            return props;
        }

        const extraContext = {
            record: {
                _name: this.props.record.resModel,
                _field: this.props.name,
            },
            parent_record: {},
        };

        const data = this.props.record.data;
        if (data && data.operating_unit_id) {
            extraContext.record.operating_unit_id = Array.isArray(
                data.operating_unit_id
            )
                ? data.operating_unit_id[0]
                : data.operating_unit_id;
        }

        if (this.props.record._parentRecord) {
            const parentData = this.props.record._parentRecord.data;
            if (parentData && parentData.operating_unit_id) {
                extraContext.parent_record.operating_unit_id = Array.isArray(
                    parentData.operating_unit_id
                )
                    ? parentData.operating_unit_id[0]
                    : parentData.operating_unit_id;
            }
        }

        props.context = {...(props.context || {}), ...extraContext};
        return props;
    },
});
