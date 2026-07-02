import logging
import uuid
from unittest.mock import PropertyMock, patch

from odoo.tests import common

_logger = logging.getLogger(__name__)


class TestOperatingUnitIsolation(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.env["base.operating.unit.isolation"]._register_hook()
        partner_id = cls.env.user.partner_id.id

        unique_code1 = f"OU1_{uuid.uuid4().hex[:8]}"
        unique_code2 = f"OU2_{uuid.uuid4().hex[:8]}"

        cls.ou1 = cls.env["operating.unit"].create(
            {"name": unique_code1, "code": unique_code1, "partner_id": partner_id}
        )
        cls.ou2 = cls.env["operating.unit"].create(
            {"name": unique_code2, "code": unique_code2, "partner_id": partner_id}
        )

    def _run_search_isolation(
        self,
        context_record,
        context_parent_record=None,
        isolation_attr_val=None,
        has_isolation_attr=True,
    ):
        Partner = self.env["res.partner"]

        class DummyField:
            pass

        if has_isolation_attr:
            DummyField.operating_unit_isolation = isolation_attr_val

        mock_fields_dict = Partner._fields.copy()
        mock_fields_dict["operating_unit_id"] = DummyField()
        mock_fields_dict["test_field"] = DummyField()

        context = {"record": context_record}
        if context_parent_record is not None:
            context["parent_record"] = context_parent_record

        Partner = Partner.with_context(**context)

        with patch.object(
            type(Partner), "_fields", new_callable=PropertyMock
        ) as mock_fields:
            mock_fields.return_value = mock_fields_dict
            with patch.object(type(Partner), "_where_calc") as mock_where_calc:
                # Return a dummy query so it doesn't crash
                mock_where_calc.return_value = None
                try:
                    Partner._search([])
                except Exception as e:
                    _logger.debug("Expected dummy error: %s", e)

                self.assertTrue(mock_where_calc.called, "_where_calc should be called")
                return mock_where_calc.call_args[0][0]

    def test_search_isolation_current_record(self):
        called_domain = self._run_search_isolation(
            context_record={
                "_name": "res.partner",
                "_field": "test_field",
                "operating_unit_id": self.ou1.id,
            },
            isolation_attr_val="operating_unit_id",
        )
        self.assertIn("|", called_domain)
        self.assertIn(("operating_unit_id", "=", False), called_domain)
        self.assertIn(("operating_unit_id", "in", [self.ou1.id]), called_domain)

    def test_search_isolation_parent_record(self):
        called_domain = self._run_search_isolation(
            context_record={
                "_name": "res.partner",
                "_field": "test_field",
            },
            context_parent_record={"operating_unit_id": self.ou2.id},
            isolation_attr_val="order_id.operating_unit_id",
        )
        self.assertIn("|", called_domain)
        self.assertIn(("operating_unit_id", "=", False), called_domain)
        self.assertIn(("operating_unit_id", "in", [self.ou2.id]), called_domain)

    def test_search_isolation_no_field_isolation_val(self):
        called_domain = self._run_search_isolation(
            context_record={
                "_name": "res.partner",
                "_field": "test_field",
                "operating_unit_id": self.ou1.id,
            },
            context_parent_record={"operating_unit_id.name": "operating_unit_id"},
            has_isolation_attr=False,
        )
        self.assertIn("|", called_domain)
        self.assertIn(("operating_unit_id", "=", False), called_domain)
        self.assertIn(("operating_unit_id", "in", [self.ou1.id]), called_domain)
