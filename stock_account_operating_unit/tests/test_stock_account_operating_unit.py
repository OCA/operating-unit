# © 2019 ForgeFlow, S.L.
# - Jordi Ballester Alomar
# © 2019 Serpent Consulting Services Pvt. Ltd. - Sudhir Arya
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from unittest.mock import patch

from odoo.exceptions import UserError
from odoo.tests import Form

from odoo.addons.stock.tests.common import TestStockCommon


class TestStockAccountOperatingUnit(TestStockCommon):
    def setUp(self):
        super().setUp()
        self.res_groups = self.env["res.groups"]
        self.res_users_model = self.env["res.users"]
        self.aml_model = self.env["account.move.line"]
        self.account_model = self.env["account.account"]
        self.product_model = self.env["product.product"]
        self.product_cteg_model = self.env["product.category"]
        self.operating_unit_model = self.env["operating.unit"]
        self.company_model = self.env["res.company"]
        self.move_model = self.env["stock.move"]
        self.picking_model = self.env["stock.picking"]

        # Company
        self.company = self.env.ref("base.main_company")
        self.group_stock_manager = self.env.ref("stock.group_stock_manager")
        self.grp_acc_user = self.env.ref("account.group_account_user")
        self.grp_stock_user = self.env.ref("stock.group_stock_user")
        # Main Operating Unit
        self.ou1 = self.env.ref("operating_unit.main_operating_unit")
        # B2B Operating Unit
        self.b2b = self.env.ref("operating_unit.b2b_operating_unit")
        # B2C Operating Unit
        self.b2c = self.env.ref("operating_unit.b2c_operating_unit")
        # Partner
        self.partner1 = self.env.ref("base.res_partner_1")
        self.stock_location_stock = self.env.ref("stock.stock_location_stock")
        self.supplier_location = self.env.ref("stock.stock_location_suppliers")

        # Create user1
        self.user1 = self._create_user(
            "stock_account_user_1",
            [self.grp_stock_user, self.grp_acc_user, self.group_stock_manager],
            self.company,
            [self.ou1, self.b2c],
        )

        # Create user2
        self.user2 = self._create_user(
            "stock_account_user_2",
            [self.grp_stock_user, self.grp_acc_user, self.group_stock_manager],
            self.company,
            [self.b2c],
        )

        # Create account for Goods Received Not Invoiced
        name = "Goods Received Not Invoiced"
        code = "grni"
        self.account_grni = self._create_account("equity", name, code, self.company)
        # Create account for Cost of Goods Sold
        name = "Cost of Goods Sold"
        code = "cogs"
        self.account_cogs_id = self._create_account("expense", name, code, self.company)
        # Create account for Inventory
        name = "Inventory"
        code = "inventory"
        self.account_inventory = self._create_account(
            "asset_current", name, code, self.company
        )
        # Create account for Inter-OU Clearing
        name = "Inter-OU Clearing"
        code = "INTEROU"
        self.account_inter_ou_clearing = self._create_account(
            "equity", name, code, self.company
        )
        # Update company data
        self.company.write(
            {
                "inter_ou_clearing_account_id": self.account_inter_ou_clearing.id,
                "ou_is_self_balanced": True,
            }
        )

        # Create Product
        self.product = self._create_product()
        # Create incoming stock picking type
        self.incoming_id = self.env.ref("stock.warehouse0").in_type_id
        # Create incoming and internal stock picking types
        b2c_wh = self.env.ref("stock_operating_unit.stock_warehouse_b2c")
        b2c_wh.lot_stock_id.write({"operating_unit_id": self.b2c.id})
        self.location_b2c_id = b2c_wh.lot_stock_id
        self.b2c_type_in_id = b2c_wh.in_type_id
        self.b2c_type_int_id = b2c_wh.int_type_id

    def _create_user(self, login, groups, company, operating_units):
        """Create a user."""
        group_ids = [group.id for group in groups]
        user = self.res_users_model.create(
            {
                "name": "Test Stock Account User",
                "login": login,
                "password": "demo",
                "email": "example@yourcompany.com",
                "company_id": company.id,
                "company_ids": [(4, company.id)],
                "operating_unit_ids": [(4, ou.id) for ou in operating_units],
                "groups_id": [(6, 0, group_ids)],
            }
        )
        return user

    def _create_account(self, acc_type, name, code, company):
        """Create an account."""
        account = self.account_model.with_company(company).create(
            {
                "name": name,
                "code": code,
                "account_type": acc_type,
            }
        )
        return account

    def _create_product(self):
        """Create a Product with inventory valuation set to auto."""
        product_cteg = self.product_cteg_model.create(
            {
                "name": "test_product_ctg",
                "property_valuation": "real_time",
                "property_cost_method": "standard",
                "property_stock_valuation_account_id": self.account_inventory.id,
                "property_stock_account_input_categ_id": self.account_grni.id,
                "property_stock_account_output_categ_id": self.account_cogs_id.id,
            }
        )
        product = self.product_model.create(
            {
                "name": "test_product",
                "categ_id": product_cteg.id,
                "type": "consu",
                "is_storable": True,
                "list_price": 1.0,
                "standard_price": 1.0,
            }
        )
        return product

    def _create_picking(self, user, ou_id, picking_type, src_loc_id, dest_loc_id):
        """Create a Picking."""
        picking = self.picking_model.with_user(user.id).create(
            {
                "picking_type_id": picking_type.id,
                "location_id": src_loc_id.id,
                "location_dest_id": dest_loc_id.id,
                "operating_unit_id": ou_id.id,
            }
        )
        self.move_model.with_user(user.id).create(
            {
                "name": "a move",
                "product_id": self.product.id,
                "product_uom_qty": 1.0,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": src_loc_id.id,
                "location_dest_id": dest_loc_id.id,
            }
        )
        return picking

    def _confirm_receive(self, user_id, picking):
        """
        Checks the stock availability,validates and process the stock picking.
        """
        picking.action_confirm()
        picking.action_assign()
        for move in picking.move_ids:
            if not move.quantity:
                move.quantity = move.product_uom_qty
        res = picking.with_user(user_id).button_validate()
        if isinstance(res, dict):
            view_id = res.get("view_id") or (res.get("views") or [(False, False)])[0][0]
            view = self.env["ir.ui.view"].browse(view_id) if view_id else False
            form = Form(
                self.env[res["res_model"]].with_context(**res.get("context", {})),
                view=view if view else None,
            )
            wiz = form.save()
            if hasattr(wiz, "process_cancel_backorder"):
                wiz.process_cancel_backorder()
            else:
                wiz.process()

    def _check_account_balance(
        self, account_id, operating_unit=None, expected_balance=0.0
    ):
        """
        Check the balance of the account based on different operating units.
        """
        domain = [("account_id", "=", account_id)]
        if operating_unit:
            domain.extend([("operating_unit_id", "=", operating_unit.id)])

        balance = self._get_balance(domain)
        if operating_unit:
            self.assertEqual(
                balance,
                expected_balance,
                f"Balance is not {expected_balance} "
                f"for Operating Unit {operating_unit.name}.",
            )
        else:
            self.assertEqual(
                balance,
                expected_balance,
                f"Balance is not {expected_balance} " "for all Operating Units.",
            )

    def _get_balance(self, domain):
        """
        Call read_group method and return the balance of particular account.
        """
        aml_rec = self.aml_model.read_group(
            domain,
            ["debit", "credit", "account_id"],
            ["account_id"],
        )
        if aml_rec:
            return aml_rec[0].get("debit", 0.0) - aml_rec[0].get("credit", 0.0)
        else:
            return 0.0

    def test_pickings(self):
        """Test account balances during receiving stock into the main
        operating unit, then into b2c operating unit, and then transfer stock
        from main ou to b2c."""
        # Create Incoming Shipment 1
        self.picking = self._create_picking(
            self.user1,
            self.ou1,
            self.incoming_id,
            self.supplier_location,
            self.stock_location_stock,
        )
        # Receive it
        self._confirm_receive(self.user1.id, self.picking)
        # GL account ‘Inventory’ has balance 1 irrespective of the OU
        expected_balance = 1.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=None,
            expected_balance=expected_balance,
        )
        # GL account ‘Inventory’ has balance 1 on OU main_operating_unit
        expected_balance = 1.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=self.ou1,
            expected_balance=expected_balance,
        )
        # GL account ‘Inventory’ has balance 0 on OU B2C
        expected_balance = 0.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=self.b2c,
            expected_balance=expected_balance,
        )
        # GL account ‘Goods Received Not Invoiced’ has balance -1
        # irrespective of the OU
        expected_balance = -1.0
        self._check_account_balance(
            self.account_grni.id,
            operating_unit=None,
            expected_balance=expected_balance,
        )

        # GL account ‘Goods Received Not Invoiced’ has balance -1 on Main OU
        expected_balance = -1.0
        self._check_account_balance(
            self.account_grni.id,
            operating_unit=self.ou1,
            expected_balance=expected_balance,
        )
        # GL account ‘Goods Received Not Invoiced’ has balance 0 on OU b2c
        expected_balance = 0.0
        self._check_account_balance(
            self.account_grni.id,
            operating_unit=self.b2c,
            expected_balance=expected_balance,
        )

        # Create Incoming Shipment 2
        self.picking = self._create_picking(
            self.user2,
            self.b2c,
            self.b2c_type_in_id,
            self.supplier_location,
            self.location_b2c_id,
        )

        # Receive it
        self._confirm_receive(self.user2.id, self.picking)

        # GL account ‘Inventory’ has balance 2 irrespective of the OU
        expected_balance = 2.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=None,
            expected_balance=expected_balance,
        )
        # GL account ‘Inventory’ has balance 1 on OU main_operating_unit
        expected_balance = 1.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=self.ou1,
            expected_balance=expected_balance,
        )
        # GL account ‘Inventory’ has balance 1 on OU b2c
        expected_balance = 1.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=self.b2c,
            expected_balance=expected_balance,
        )

        # GL account ‘Goods Received Not Invoiced’ has balance -2
        # irrespective of the OU
        expected_balance = -2.0
        self._check_account_balance(
            self.account_grni.id,
            operating_unit=None,
            expected_balance=expected_balance,
        )
        # GL account ‘Goods Received Not Invoiced’ has balance -1 on Main OU
        expected_balance = -1.0
        self._check_account_balance(
            self.account_grni.id,
            operating_unit=self.ou1,
            expected_balance=expected_balance,
        )
        # GL account ‘Goods Received Not Invoiced’ has balance -1 on OU b2c
        expected_balance = -1.0
        self._check_account_balance(
            self.account_grni.id,
            operating_unit=self.b2c,
            expected_balance=expected_balance,
        )

        # Create Internal Transfer
        self.picking = self._create_picking(
            self.user1,
            self.b2c,
            self.b2c_type_int_id,
            self.stock_location_stock,
            self.location_b2c_id,
        )
        # Receive it
        self._confirm_receive(self.user1.id, self.picking)
        # GL account ‘Inventory’ has balance 2 irrespective of the OU
        expected_balance = 2.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=None,
            expected_balance=expected_balance,
        )
        # GL account ‘Inventory’ has balance 0 on OU main_operating_unit
        expected_balance = 0.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=self.ou1,
            expected_balance=expected_balance,
        )
        # GL account ‘Inventory’ has balance 2 on OU b2c
        expected_balance = 2.0
        self._check_account_balance(
            self.account_inventory.id,
            operating_unit=self.b2c,
            expected_balance=expected_balance,
        )
        # GL account ‘Inter-OU clearing’ has balance 0 irrespective of the OU
        expected_balance = 0.0
        self._check_account_balance(
            self.account_inter_ou_clearing.id,
            operating_unit=None,
            expected_balance=expected_balance,
        )

    def test_confirm_receive_processes_backorder_wizard_action(self):
        picking = self._create_picking(
            self.user1,
            self.ou1,
            self.incoming_id,
            self.supplier_location,
            self.stock_location_stock,
        )
        picking.action_confirm()
        picking.action_assign()
        picking.move_ids.quantity = 0.5
        self._confirm_receive(self.user1.id, picking)
        self.assertEqual(picking.state, "done")

    def test_generate_valuation_lines_data_inter_ou_account_mismatch_raises(self):
        b2c_wh = self.env.ref("stock_operating_unit.stock_warehouse_b2c")
        src_location = self.env["stock.location"].create(
            {
                "name": "OU1 Stock Location",
                "usage": "internal",
                "company_id": self.company.id,
                "operating_unit_id": self.ou1.id,
            }
        )
        dest_location = self.env["stock.location"].create(
            {
                "name": "B2C Stock Location",
                "usage": "internal",
                "company_id": self.company.id,
                "operating_unit_id": self.b2c.id,
            }
        )
        picking = self.picking_model.create(
            {
                "picking_type_id": b2c_wh.int_type_id.id,
                "location_id": src_location.id,
                "location_dest_id": dest_location.id,
            }
        )
        move = self.move_model.create(
            {
                "name": "a move",
                "product_id": self.product.id,
                "product_uom_qty": 1.0,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": src_location.id,
                "location_dest_id": dest_location.id,
            }
        )

        mocked_res = {
            "debit_line_vals": {"account_id": self.account_inventory.id},
            "credit_line_vals": {"account_id": self.account_grni.id},
        }
        with patch(
            "odoo.addons.stock_account.models.stock_move.StockMove._generate_valuation_lines_data",
            return_value=mocked_res,
        ):
            with self.assertRaises(UserError):
                move._generate_valuation_lines_data(
                    partner_id=False,
                    qty=1.0,
                    debit_value=1.0,
                    credit_value=1.0,
                    debit_account_id=self.account_inventory.id,
                    credit_account_id=self.account_grni.id,
                    svl_id=False,
                    description="Test",
                )

    def test_generate_valuation_lines_data_uses_warehouse_ou_when_move_has_no_ou(self):
        b2c_wh = self.env.ref("stock_operating_unit.stock_warehouse_b2c")
        internal_location = self.env["stock.location"].create(
            {
                "name": "No OU Stock Location",
                "usage": "internal",
                "company_id": self.company.id,
            }
        )
        picking = self.picking_model.create(
            {
                "picking_type_id": b2c_wh.in_type_id.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": internal_location.id,
            }
        )
        move = self.move_model.create(
            {
                "name": "a move",
                "product_id": self.product.id,
                "product_uom_qty": 1.0,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": internal_location.id,
            }
        )

        mocked_res = {
            "debit_line_vals": {"account_id": self.account_inventory.id},
            "credit_line_vals": {"account_id": self.account_inventory.id},
        }
        with patch(
            "odoo.addons.stock_account.models.stock_move.StockMove._generate_valuation_lines_data",
            return_value=mocked_res,
        ):
            rslt = move._generate_valuation_lines_data(
                partner_id=False,
                qty=1.0,
                debit_value=1.0,
                credit_value=1.0,
                debit_account_id=self.account_inventory.id,
                credit_account_id=self.account_inventory.id,
                svl_id=False,
                description="Test",
            )
        self.assertEqual(
            rslt["debit_line_vals"]["operating_unit_id"],
            b2c_wh.operating_unit_id.id,
        )
        self.assertEqual(
            rslt["credit_line_vals"]["operating_unit_id"],
            b2c_wh.operating_unit_id.id,
        )

    def test_generate_valuation_lines_data_sets_price_diff_operating_unit(self):
        b2c_wh = self.env.ref("stock_operating_unit.stock_warehouse_b2c")
        src_location = self.env["stock.location"].create(
            {
                "name": "OU1 Stock Location (Price Diff)",
                "usage": "internal",
                "company_id": self.company.id,
                "operating_unit_id": self.ou1.id,
            }
        )
        dest_location = self.env["stock.location"].create(
            {
                "name": "B2C Stock Location (Price Diff)",
                "usage": "internal",
                "company_id": self.company.id,
                "operating_unit_id": self.b2c.id,
            }
        )
        picking = self.picking_model.create(
            {
                "picking_type_id": b2c_wh.int_type_id.id,
                "location_id": src_location.id,
                "location_dest_id": dest_location.id,
            }
        )
        move = self.move_model.create(
            {
                "name": "a move",
                "product_id": self.product.id,
                "product_uom_qty": 1.0,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": src_location.id,
                "location_dest_id": dest_location.id,
            }
        )

        mocked_res = {
            "debit_line_vals": {"account_id": self.account_inventory.id},
            "credit_line_vals": {"account_id": self.account_inventory.id},
            "price_diff_line_vals": {"account_id": self.account_grni.id},
        }
        with patch(
            "odoo.addons.stock_account.models.stock_move.StockMove._generate_valuation_lines_data",
            return_value=mocked_res,
        ):
            rslt = move._generate_valuation_lines_data(
                partner_id=False,
                qty=1.0,
                debit_value=2.0,
                credit_value=1.0,
                debit_account_id=self.account_inventory.id,
                credit_account_id=self.account_inventory.id,
                svl_id=False,
                description="Test",
            )
        self.assertEqual(
            rslt["price_diff_line_vals"]["operating_unit_id"],
            self.ou1.id,
        )

    def test_generate_valuation_lines_data_passthrough_when_parent_returns_falsy(self):
        b2c_wh = self.env.ref("stock_operating_unit.stock_warehouse_b2c")
        picking = self.picking_model.create(
            {
                "picking_type_id": b2c_wh.in_type_id.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": self.stock_location_stock.id,
            }
        )
        move = self.move_model.create(
            {
                "name": "a move",
                "product_id": self.product.id,
                "product_uom_qty": 1.0,
                "product_uom": self.product.uom_id.id,
                "picking_id": picking.id,
                "location_id": self.supplier_location.id,
                "location_dest_id": self.stock_location_stock.id,
            }
        )

        with patch(
            "odoo.addons.stock_account.models.stock_move.StockMove._generate_valuation_lines_data",
            return_value=False,
        ):
            rslt = move._generate_valuation_lines_data(
                partner_id=False,
                qty=1.0,
                debit_value=1.0,
                credit_value=1.0,
                debit_account_id=self.account_inventory.id,
                credit_account_id=self.account_inventory.id,
                svl_id=False,
                description="Test",
            )
        self.assertFalse(rslt)
