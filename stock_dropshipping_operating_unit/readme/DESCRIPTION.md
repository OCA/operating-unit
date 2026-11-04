This module propagates the Operating Unit of a Sale Order (SO) to the
Purchase Orders that are automatically generated for Dropship SO lines.

The module handles both shared and dedicated warehouses:

- If the warehouse has no Operating Unit (shared warehouse), the
  Sale Order's Operating Unit is used as a fallback.
- If the warehouse has a specific Operating Unit, that warehouse Operating Unit
  takes precedence (existing behaviour of `purchase_stock_operating_unit` module).
