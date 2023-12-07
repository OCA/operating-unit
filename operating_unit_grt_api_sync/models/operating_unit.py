import logging
import os

import requests

from odoo import fields, models

_logger = logging.getLogger(__name__)


class OperatingUnit(models.Model):
    _inherit = "operating.unit"

    synced_with_grt = fields.Boolean(
        "Is Synced with GRT API", default=False, readonly=True
    )

    def _sync_branches_data_with_grt(self):
        def _fetch_grt_data():
            api_key = os.environ.get("GRT_API_KEY")
            if not api_key:
                _logger.error("GRT API Sync: API key has not been provided.")
                return
            url = "https://grt-api.azurewebsites.net/v1/grt/management_ids/flat"
            headers = {"Authorization": f"Bearer {api_key}"}
            try:
                _logger.info("GRT API Sync: Requesting data from GRT API.")
                r = requests.get(url, headers=headers, timeout=30)
                if r.status_code == 200:
                    _logger.info("GRT API Sync: Requesting data from GRT API.")
                    return r.json()
                else:
                    error_message = r.json().get("detail")
                    _logger.error(
                        f"GRT API Sync: Request to GRT API failed with "
                        f"status code {r.status_code}: {error_message}."
                    )
            except Exception as e:
                _logger.error(
                    f"GRT API Sync: Request to GRT API failed with error {e}."
                )

        if data := _fetch_grt_data():  # noqa: E231 E701
            self._process_grt_branch_data(data)

    def _create_new_branches(self, branches_data, ou_code_company_mappings):
        def _prepare_vals(data):
            branch = (
                data["l5_branch"]
                if data["l5_branch"] == "OU Office"
                else f"Branch {data['l5_branch']}"
            )
            name = f"{data['management_id']} - OU {data['l8_operating_unit']}, {branch}"
            code_prefix = data["management_id"][:3]
            company = ou_code_company_mappings.filtered(
                lambda m: m.code_prefix == code_prefix
            ).company_id
            return {
                "name": name,
                "code": data["management_id"],
                "company_id": company.id,
                "valid_from": data["operational_from"],
                "valid_until": data["operational_until"],
                "synced_with_grt": True,
            }

        def _prepare_partner_vals(data):
            branch = (
                data["l5_branch"]
                if data["l5_branch"] == "OU Office"
                else f"Branch {data['l5_branch']}"
            )
            country = self.env["res.country"].search(
                [("name", "=", data["l10_operating_country"])]
            )
            return {
                "name": f"OU {data['l8_operating_unit']}, {branch}",
                "city": data["l5_branch"],
                "country_id": country.id if country else False,
            }

        vals = []
        partner_vals = []
        for branch_data in branches_data:
            create_vals = _prepare_vals(branch_data)
            vals.append(create_vals)
            partner_create_vals = _prepare_partner_vals(branch_data)
            partner_vals.append(partner_create_vals)
        partners = self.env["res.partner"].create(partner_vals)
        vals_with_partner = []
        for partner, mid in zip(partners, vals):
            mid.update({"partner_id": partner.id})
            vals_with_partner.append(mid)
        self.create(vals_with_partner)

    def _process_grt_branch_data(self, data):

        ou_code_company_mappings = self.env["operating.unit.company.mapping"].search([])

        def _filter_branches_data():
            available_prefixes = ou_code_company_mappings.mapped("code_prefix")
            return [
                d
                for d in data
                if d["management_id"][:3] in available_prefixes
                and d["management_id_level"] == "Branch"
            ]

        def _filter_branches_to_update(recs, data):
            """Filter the recordset to only include records that need to be updated."""
            return recs.filtered(
                lambda mid: mid.valid_from != data[mid.code]["operational_from"]
                or mid.valid_until != data[mid.code]["operational_until"]
                or not mid.synced_with_grt
            )

        def _update_branch(recs, branch_data):
            for rec in recs:
                data = branch_data[rec.code]
                vals = {}
                if rec.valid_from != data["operational_from"]:
                    vals["valid_from"] = data["operational_from"]
                if rec.valid_until != data["operational_until"]:
                    vals["valid_until"] = data["operational_until"]
                if not rec.synced_with_grt:
                    vals["synced_with_grt"] = True
                if vals:
                    rec.write(vals)

        if data := _filter_branches_data():  # noqa: E231 E701

            branches_codes = [d["management_id"] for d in data]
            branches = self.search([("code", "in", branches_codes)])
            branch_codes = branches.mapped("code")

            if branches_create_data := [  # noqa: E231 E701
                d for d in data if d["management_id"] not in branch_codes
            ]:
                self._create_new_branches(
                    branches_create_data, ou_code_company_mappings
                )

            if data != branches_create_data:
                branches_to_update_data = {
                    d["management_id"]: d for d in data if d not in branches_create_data
                }

                if branches_to_unsync := branches.filtered(  # noqa: E231 E701
                    lambda mid: mid.code not in branches_to_update_data
                ):
                    branches_to_unsync.filtered(lambda b: b.synced_with_grt).write(
                        {"synced_with_grt": False}
                    )
                    branches_to_update = branches - branches_to_unsync
                else:
                    branches_to_update = branches

                branches_to_update = _filter_branches_to_update(
                    branches_to_update, branches_to_update_data
                )
                _update_branch(branches_to_update, branches_to_update_data)
