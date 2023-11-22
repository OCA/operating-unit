odoo.define("operating_unit_validity_date.relational_fields", function(require) {
    "use strict";

    var relational_fields = require("web.relational_fields");
    var FieldMany2One = relational_fields.FieldMany2One;
    var FormFieldMany2ManyTags = relational_fields.FormFieldMany2ManyTags;
    var _t = require("web.core")._t;

    var getSpan = () => {
        var $span = $(
            '<span class="fa fa-exclamation-triangle o_validity_date_icon"/>'
        );
        $span.hide();
        return $span;
    };

    var updateSpan = ($span, validity_state) => {
        $span.removeClass("o_validity_date_warning");
        $span.removeClass("o_validity_date_error");
        if (validity_state === "expired") {
            $span.attr(
                "title",
                _t("The validity date of this Operating Unit has expired.")
            );
            $span.addClass("o_validity_date_error");
            $span.show();
        } else if (validity_state === "soon_expire") {
            $span.attr(
                "title",
                _t("The validity date of this Operating Unit will soon expire.")
            );
            $span.addClass("o_validity_date_warning");
            $span.show();
        } else if (validity_state === "not_valid_yet") {
            $span.attr("title", _t("This Operating Unit is not valid yet."));
            $span.addClass("o_validity_date_error");
            $span.show();
        } else {
            $span.hide();
        }
    };

    FormFieldMany2ManyTags.include({
        init: function() {
            this._super.apply(this, arguments);
            this.checkOperatingUnitValidity =
                this.field.relation === "operating.unit" &&
                this.formatType === "one2many";
            this.operatingUnitValidityWarnings = {};
            if (this.checkOperatingUnitValidity) {
                this._updateOperatingUnitValidityWarning(this.value.res_ids);
            }
        },
        _addTag: function(data) {
            if (this.checkOperatingUnitValidity) {
                this._createOperatingUnitValidtyWarning(data.id);
                this._updateOperatingUnitValidityWarning([data.id]);
            }
            this._super.apply(this, arguments);
        },
        _createOperatingUnitValidtyWarning: function(id) {
            if (!this.operatingUnitValidityWarnings[id]) {
                this.operatingUnitValidityWarnings[id] = getSpan();
            }
        },
        _renderTags: function() {
            this._super();
            if (this.checkOperatingUnitValidity) {
                this.value.res_ids.forEach(id => {
                    this._createOperatingUnitValidtyWarning(id);
                    this.$el
                        .find(`[data-id=${id}]`)
                        .prepend(this.operatingUnitValidityWarnings[id]);
                });
            }
        },
        _updateOperatingUnitValidityWarning: function(ids) {
            var self = this;
            this._rpc({
                model: "operating.unit",
                method: "read",
                args: [ids, ["validity_state"]],
            }).then(function(result) {
                result.forEach(data => {
                    updateSpan(
                        self.operatingUnitValidityWarnings[data.id],
                        data.validity_state
                    );
                });
            });
        },
    });

    FieldMany2One.include({
        init: function() {
            this._super.apply(this, arguments);
            this.checkOperatingUnitValidity =
                this.field.relation === "operating.unit" &&
                this.formatType === "many2one";
            if (this.checkOperatingUnitValidity) {
                this.$operatingUnitValidityWarning = getSpan();
                this._updateOperatingUnitValidityWarning(this.value.res_id);
            }
        },
        _renderReadonly: function() {
            this._super();
            if (this.checkOperatingUnitValidity) {
                this.$el.append(this.$operatingUnitValidityWarning);
            }
        },
        _renderEdit: function() {
            this._super();
            if (this.checkOperatingUnitValidity) {
                this.$operatingUnitValidityWarning.insertAfter(this.$input);
            }
        },
        _updateOperatingUnitValidityWarning: function(id) {
            var self = this;
            if (id === undefined) {
                self.$operatingUnitValidityWarning.hide();
            } else {
                this._rpc({
                    model: "operating.unit",
                    method: "read",
                    args: [id, ["validity_state"]],
                }).then(function(result) {
                    if (result[0]) {
                        updateSpan(
                            self.$operatingUnitValidityWarning,
                            result[0].validity_state
                        );
                    }
                });
            }
        },
        _onFieldChanged: function() {
            this._super();
            if (this.checkOperatingUnitValidity) {
                this._updateOperatingUnitValidityWarning(this.lastSetValue.id);
            }
        },
    });
});
