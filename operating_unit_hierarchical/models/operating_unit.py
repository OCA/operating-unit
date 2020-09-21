# Copyright 2020 Hunki Enterprises BV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class OperatingUnit(models.Model):
    _inherit = "operating.unit"
    _parent_store = True
    _order = "parent_level asc, name asc"

    parent_id = fields.Many2one("operating.unit", index=True)
    parent_path = fields.Char(index=True)
    parent_level = fields.Integer(index=True)

    def _parent_level_compute(self):
        query = (  # pylint: disable=sql-injection
            "update operating_unit set parent_level = "
            "array_length(regexp_split_to_array(parent_path, '/'), 1) - 2"
            "%s"
        ) % (" where id in %s" if self else "")

        self.env.cr.execute(query, (tuple(self.ids),) if self else ())
        self.modified(["parent_level"])
        self.invalidate_cache(["parent_level"])

    def _parent_store_compute(self):
        result = super()._parent_store_compute()
        self._parent_level_compute()
        return result

    def _parent_store_create(self):
        result = super()._parent_store_create()
        self._parent_level_compute()
        return result

    def _parent_store_update(self):
        result = super()._parent_store_update()
        self._parent_level_compute()
        return result

    def name_get(self):
        return [
            (
                this.id,
                " / ".join(
                    self.browse(
                        map(int, filter(None, this.parent_path.split("/")))
                    ).mapped("name")
                ),
            )
            for this in self
        ]
