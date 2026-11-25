# Copyright 2017-2026 CIT Services
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import api, models


class BaseOperatingUnitIsolation(models.AbstractModel):
    _name = "base.operating.unit.isolation"
    _description = "Extend AbstractModel for Operation Unit Isolation"

    def _register_hook(self):
        res = super()._register_hook()
        ou_patched = getattr(models.BaseModel, "ou_patched", False)
        if not ou_patched:
            origin_search = models.BaseModel._search

            @api.model
            def _ou_search(self, domain, *args, **kwargs):
                record = self.env.context.get("record")

                ou_field = False
                if "operating_unit_id" in self._fields:
                    ou_field = "operating_unit_id"
                elif "operating_unit_ids" in self._fields:
                    ou_field = "operating_unit_ids"

                if (
                    record
                    and ou_field
                    and record.get("_field")
                    and "_name" in record
                    and record["_name"] in self.env
                    and record["_field"] in self.env[record["_name"]]._fields
                ):
                    fld = self.env[record["_name"]]._fields[record["_field"]]

                    isolation_val = getattr(fld, "operating_unit_isolation", False)
                    filter_ou = False

                    if isolation_val:
                        isolation = isolation_val.split(".")
                        if len(isolation) == 2:
                            parent_record = self.env.context.get("parent_record", {})
                            filter_ou = parent_record.get(isolation[1])
                        elif len(isolation) == 1:
                            filter_ou = record.get(isolation[0])
                    else:
                        if "operating_unit_id" in record:
                            filter_ou = record.get("operating_unit_id")
                        else:
                            parent_record = self.env.context.get("parent_record", {})
                            if parent_record and "operating_unit_id" in parent_record:
                                filter_ou = parent_record.get("operating_unit_id")

                    if filter_ou:
                        domain = list(domain) if domain else []
                        domain.extend(
                            [
                                "|",
                                (ou_field, "=", False),
                                (ou_field, "in", [filter_ou]),
                            ]
                        )

                return origin_search(self, domain, *args, **kwargs)

            models.BaseModel._search = _ou_search
            models.BaseModel.ou_patched = True

        return res
