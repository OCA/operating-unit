# Copyright 2023 Ecosoft Co., Ltd. (http://ecosoft.co.th)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from odoo.tests import tagged
from odoo.tests.common import Form

from odoo.addons.account_asset_operating_unit.tests.test_account_asset_operating_unit import (
    TestAccountAssetOperatingUnit,
)


@tagged("post_install", "-at_install")
class TestAssetTransferOperatingUnit(TestAccountAssetOperatingUnit):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Journal
        cls.journal_misc_transfer = cls.env["account.journal"].search(
            [("company_id", "=", cls.env.company.id), ("type", "=", "general")], limit=1
        )

    def test_01_asset_transfer_auc_to_asset(self):
        """Create AUC and then transfer to normal asset class,
        I expect a new journal entry will be created"""
        self.asset1.method_number = 0
        self.asset1.validate()
        self.asset1.invalidate_cache()
        # can_transfer = True after validate
        self.assertTrue(list(set(self.asset1.mapped("can_transfer")))[0])

        # Create Asset Transfer
        with Form(
            self.env["account.asset.transfer"].with_context(active_ids=self.asset1.ids)
        ) as t:
            t.transfer_journal_id = self.journal_misc_transfer
            with t.to_asset_ids.new() as to_asset:
                to_asset.asset_name = "Asset 1"
                to_asset.asset_profile_id = self.profile_id
                to_asset.quantity = 1
                to_asset.price_unit = 500
                to_asset.operating_unit_id = self.b2c_OU
            with t.to_asset_ids.new() as to_asset:
                to_asset.asset_name = "Asset 2"
                to_asset.asset_profile_id = self.profile_id
                to_asset.quantity = 1
                to_asset.price_unit = 500
        transfer_wiz = t.save()
        # Test expand asset lines from quantity line
        self.assertEqual(len(transfer_wiz.to_asset_ids), 2)
        self.assertEqual(transfer_wiz.operating_unit_id, self.asset1.operating_unit_id)
        self.assertEqual(transfer_wiz.to_asset_ids[0].operating_unit_id, self.b2c_OU)
        self.assertEqual(
            transfer_wiz.to_asset_ids[1].operating_unit_id,
            self.asset1.operating_unit_id,
        )
        res = transfer_wiz.transfer()
        transfer_move = self.env["account.move"].browse(res["domain"][0][2])
        assets = transfer_move.invoice_line_ids.mapped("asset_id")
        self.assertEqual(transfer_move.operating_unit_id, self.asset1.operating_unit_id)
        # 2 new assets created, and value equal to original assets
        new_assets = assets.filtered(lambda l: l.state == "draft")
        self.assertEqual(sum(new_assets.mapped("purchase_value")), 1000)
        self.assertEqual(new_assets.operating_unit_id, self.asset1.operating_unit_id)
