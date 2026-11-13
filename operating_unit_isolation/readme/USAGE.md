To use this functionality in your own module, add the
`operating_unit_isolation` property to the field definitions in your
models.

**Isolating based on the current record's Operating Unit:**

If you have a field on a model and you want the selectable records to be
restricted to the same Operating Unit as the current record, use the
field name of the operating unit as the value:

``` python
from odoo import fields, models

class CustomModel(models.Model):
    _name = "custom.model"

    operating_unit_id = fields.Many2one("operating.unit", "Operating Unit")

    # This will restrict selectable partners to those matching the
    # 'operating_unit_id' of this custom.model record (or those without an OU)
    partner_id = fields.Many2one(
        "res.partner",
        string="Partner",
        operating_unit_isolation="operating_unit_id"
    )
```

**Isolating based on a parent record's Operating Unit (One2many
context):**

If you are working within a One2many line (e.g., `sale.order.line`) and
want to filter the relation based on the parent model's Operating Unit,
specify the relational field name to the parent and the parent's
operating unit field name separated by a dot:

``` python
from odoo import fields, models

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    # This will restrict selectable products to those matching the 
    # 'operating_unit_id' on the parent 'sale.order' (linked via order_id)
    product_id = fields.Many2one(
        "product.product",
        string="Product",
        operating_unit_isolation="order_id.operating_unit_id"
    )
```

## Technical Details

- **Frontend**: Overrides the base OWL `Field` component's props to pass
  the `record` and `parent_record` along with their `operating_unit_id`
  into the RPC context.
- **Backend**: Safely monkey-patches `models.BaseModel._search` to
  intercept the domain and append an operating unit restriction if
  the targeted field specifies the `operating_unit_isolation` property.
  - **Dynamic Field Detection**: Automatically detects if the target model
    uses a Many2one (`operating_unit_id`) or Many2many (`operating_unit_ids`)
    field for its operating unit.
  - **Empty Value Handling**: Explicitly includes an `OR` condition allowing
    records with no assigned operating unit (`False`) to be universally
    selectable.
  - **Automatic Fallback**: Automatically applies the `operating_unit_id`
    isolation natively, without requiring the property to be explicitly defined
    on the field. It uses the parent model's operating unit when the child model
    doesn't have one.
