An extension to provide dynamic isolation for operating units across
models.

This module ensures that users can only select related records that
belong to the same Operating Unit as the current record or its parent
record. It achieves this by seamlessly injecting the current record and
parent record state from the frontend (Odoo 18 OWL framework) into the
backend `_search` operations.

When a user attempts to search or select a record for a relation (e.g.,
in a dropdown autocomplete), this module will dynamically filter the
available options based on the `operating_unit_id` of the active record.

This isolation is triggered automatically for any relation field that
specifies the `operating_unit_isolation` attribute.
