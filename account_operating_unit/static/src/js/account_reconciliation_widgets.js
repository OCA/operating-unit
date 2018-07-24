odoo.define('account_operating_unit.reconciliation', function (require) {
"use strict";

    // require original module JS
    var core = require('web.core');
    var _t = core._t;
    var FieldMany2One = core.form_widget_registry.get('many2one');

    var reconciliation = require('account.reconciliation');
    reconciliation.abstractReconciliation.include({

        init: function(parent, context) {
            this._super(parent);
            this.create_form_fields['operating_unit_id'] = {
                id: "operating_unit_id",
                index: 0, // position in the form
                corresponding_property: "operating_unit_id", // a account.move.line field name
                label: _t("Operating Unit"),
                required: false,
                group:"operating_unit.group_multi_operating_unit",
                constructor: FieldMany2One,
                field_properties: {
                    relation: "operating.unit",
                    string: _t("Operating Unit"),
                    type: "many2one",
                    domain: [],
                },
            }
        },

        fetchPresets: function() {
            var self = this;
            var deferred_last_update = self.model_presets.query(['write_date']).order_by('-write_date').first().then(function (data) {
                self.presets_last_write_date = (data ? data.write_date : undefined);
            });
            var deferred_presets = self.model_presets.query().order_by('-sequence', '-id').all().then(function (data) {
                self.presets = {};
                _(data).each(function(datum){
                    var operating_unit = datum.journal_id.operating_unit_id
                    self.model_presets.call("get_operating_unit", [datum['id']]).then(function(result){
                        operating_unit = result['operating_unit_id']
                        var preset = {
                            id: datum.id,
                            name: datum.name,
                            sequence: datum.sequence,
                            lines: [{
                                account_id: datum.account_id,
                                journal_id: datum.journal_id,
                                label: datum.label,
                                amount_type: datum.amount_type,
                                amount: datum.amount,
                                tax_id: datum.tax_id,
                                analytic_account_id: datum.analytic_account_id,
                                operating_unit_id: operating_unit,
                            }]
                        };
                        if (datum.has_second_line) {
                            preset.lines.push({
                                account_id: datum.second_account_id,
                                journal_id: datum.second_journal_id,
                                label: datum.second_label,
                                amount_type: datum.second_amount_type,
                                amount: datum.second_amount,
                                tax_id: datum.second_tax_id,
                                analytic_account_id: datum.second_analytic_account_id,
                                operating_unit_id:operating_unit,
                            });
                        }
                        self.presets[datum.id] = preset;
                    });

                });
            });
            return $.when(deferred_last_update, deferred_presets);
        }
    })

    reconciliation.abstractReconciliationLine.include({

        prepareCreatedMoveLinesForPersisting: function(lines) {
            lines = _.filter(lines, function(line) { return !line.is_tax_line });
            return _.collect(lines, function(line) {
                var dict = {
                    account_id: line.account_id,
                    name: line.label
                };
                // Use amount_before_tax since the amount of the newly created line is adjusted to
                // reflect tax included in price in account_move_line.create()
                var amount = line.tax_id ? line.amount_before_tax: line.amount;
                dict['credit'] = (amount > 0 ? amount : 0);
                dict['debit'] = (amount < 0 ? -1 * amount : 0);
                if (typeof line.operating_unit_id !== 'undefined') {
                    dict['operating_unit_id'] = line.operating_unit_id;
                }
                if (line.tax_id) dict['tax_ids'] = [[4, line.tax_id, null]];
                if (line.analytic_account_id) dict['analytic_account_id'] = line.analytic_account_id;
                return dict;
            });
        },

        initializeCreateForm: function(){
            this._super();
            if (typeof this.operating_unit_id_field !== 'undefined') {
                this.operating_unit_id_field.set("value", this.st_line['operating_unit_id']);
            }
        }
    })

});

