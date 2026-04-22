from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestEstatePropertyType(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.partner = cls.env["res.partner"].create({
            "name": "Partner Type Test",
        })

    def _create_property_type(self, **extra_vals):
        vals = {"name": "Property Type Test"}
        vals.update(extra_vals)
        return self.env["estate.property.type"].create(vals)

    def _create_property(self, property_type, **extra_vals):
        vals = {
            "name": "Property for Type Test",
            "expected_price": 1000000.0,
            "property_type_id": property_type.id,
        }
        vals.update(extra_vals)
        return self.env["estate.property"].create(vals)

    def _create_offer(self, property_record, **extra_vals):
        vals = {
            "name": "Offer Type Test",
            "price": 900000.0,
            "property_id": property_record.id,
            "partner_id": self.partner.id,
        }
        vals.update(extra_vals)
        return self.env["estate.property.offer"].create(vals)

    def test_create_property_type_success(self):
        property_type = self._create_property_type(name="Residential Type")
        self.assertTrue(property_type.exists())
        self.assertEqual(property_type.name, "Residential Type")

    def test_property_type_name_must_be_unique(self):
        self._create_property_type(name="Duplicate Type")
        with self.assertRaises(Exception) as ctx:
            self._create_property_type(name="Duplicate Type")
        self.assertIsInstance(ctx.exception, (ValidationError, IntegrityError))

    def test_compute_offer_count_from_related_properties(self):
        property_type = self._create_property_type(name="Offer Count Type")
        property_one = self._create_property(property_type, name="Property A")
        property_two = self._create_property(property_type, name="Property B")

        self._create_offer(property_one, price=850000.0)
        self._create_offer(property_two, price=880000.0)
        self._create_offer(property_two, price=930000.0)

        self.assertEqual(property_type.offer_count, 3)

    def test_action_view_offers_returns_expected_action(self):
        property_type = self._create_property_type(name="Action Type")
        action = property_type.action_view_offers()

        self.assertEqual(action.get("type"), "ir.actions.act_window")
        self.assertEqual(action.get("res_model"), "estate.property.offer")
        self.assertEqual(action.get("view_mode"), "list,form")
        self.assertEqual(action.get("target"), "current")
        self.assertEqual(action.get("domain"), [("property_type_id", "=", property_type.id)])
