# Copyright 2021 Ecosoft Co., Ltd (http://ecosoft.co.th/)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AssetReportXlsx(models.AbstractModel):
    _inherit = "report.account_asset_management.asset_report_xls"

    def _get_asset_template(self):
        asset_template = super()._get_asset_template()
        asset_template.update(
            {
                "operating_unit": {
                    "header": {"type": "string", "value": self._("Operating Unit")},
                    "asset": {
                        "type": "string",
                        "value": self._render(
                            "asset.operating_unit_id.display_name or ''"
                        ),
                    },
                    "width": 20,
                }
            }
        )
        return asset_template

    def _get_assets(self, wiz, data):
        super()._get_assets(wiz, data)
        if wiz.operating_unit_id:
            # Filter asset by operating unit
            assets = data["assets"]
            assets_by_ou = assets.filtered(
                lambda a: not a.operating_unit_id
                or a.operating_unit_id == wiz.operating_unit_id
            )
            data["assets"] = assets_by_ou
            # Filter group asset by operating unit
            grouped_assets = data["grouped_assets"]
            for k in grouped_assets.keys():
                grouped_asset = grouped_assets[k]
                assets_by_group = grouped_asset["assets"]
                grouped_asset_by_ou = assets_by_group.filtered(
                    lambda a: not a.operating_unit_id
                    or a.operating_unit_id == wiz.operating_unit_id
                )
                grouped_assets[k] = {"assets": grouped_asset_by_ou}
