from odoo.exceptions import UserError, ValidationError
from odoo.tests import TransactionCase
from psycopg2 import IntegrityError


class TestEstateProperty(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property_type = cls.env["estate.property.type"].create({
            "name": "Residential",
        })
        cls.partner = cls.env["res.partner"].create({
            "name": "Buyer Test",
        })

    def _create_property(self, **extra_vals):
        vals = {
            "name": "Property Test",
            "expected_price": 1000000.0,
            "property_type_id": self.property_type.id,
        }
        vals.update(extra_vals)
        return self.env["estate.property"].create(vals)

    def _create_offer(self, property_record, price=900000.0):
        return self.env["estate.property.offer"].create({
            "name": "Offer Test",
            "price": price,
            "property_id": property_record.id,
            "partner_id": self.partner.id,
        })

    def test_create_property_without_offer_sets_state_new(self):
        property_record = self._create_property()
        self.assertEqual(property_record.state, "new")

    def test_sql_constraint_expected_price_must_be_positive(self):
        with self.assertRaises(Exception) as ctx:
            self._create_property(expected_price=0.0)
        self.assertIsInstance(ctx.exception, (ValidationError, IntegrityError))

    def test_sql_constraint_selling_price_must_be_positive(self):
        property_record = self._create_property()
        with self.assertRaises(Exception) as ctx:
            property_record.write({"selling_price": 0.0})
        self.assertIsInstance(ctx.exception, (ValidationError, IntegrityError))

    def test_check_selling_price_constraint_rejects_under_or_equal_80_percent(self):
        property_record = self._create_property(expected_price=1000000.0)
        with self.assertRaises(ValidationError):
            property_record.write({"selling_price": 800000.0})

    def test_check_selling_price_constraint_accepts_above_80_percent(self):
        property_record = self._create_property(expected_price=1000000.0)
        property_record.write({"selling_price": 810000.0})
        self.assertEqual(property_record.selling_price, 810000.0)

    def test_compute_total_area(self):
        property_record = self._create_property(living_area=120, garden_area=30)
        self.assertEqual(property_record.total_area, 150)

    def test_compute_best_price_without_offer(self):
        property_record = self._create_property()
        self.assertEqual(property_record.best_price, 0.0)

    def test_compute_best_price_with_offers(self):
        property_record = self._create_property()
        self._create_offer(property_record, price=700000.0)
        self._create_offer(property_record, price=950000.0)
        self.assertEqual(property_record.best_price, 950000.0)

    def test_onchange_garden_sets_default_area_and_orientation(self):
        property_record = self.env["estate.property"].new({"garden": True})
        property_record._onchange_garden()
        self.assertEqual(property_record.garden_area, 50)
        self.assertEqual(property_record.garden_orientation, "north")

    def test_onchange_garden_false_does_not_override_existing_values(self):
        property_record = self.env["estate.property"].new({
            "garden": False,
            "garden_area": 120,
            "garden_orientation": "south",
        })
        property_record._onchange_garden()
        self.assertEqual(property_record.garden_area, 120)
        self.assertEqual(property_record.garden_orientation, "south")

    def test_act_btn_sold_raises_if_state_canceled(self):
        property_record = self._create_property()
        property_record.write({"state": "canceled"})
        with self.assertRaises(UserError):
            property_record.act_btn_sold()

    def test_act_btn_sold_sets_state_sold(self):
        property_record = self._create_property()
        property_record.act_btn_sold()
        self.assertEqual(property_record.state, "sold")

    def test_act_btn_cancel_raises_if_state_sold(self):
        property_record = self._create_property()
        property_record.write({"state": "sold"})
        with self.assertRaises(UserError):
            property_record.act_btn_cancel()

    def test_act_btn_cancel_sets_state_canceled(self):
        property_record = self._create_property()
        property_record.act_btn_cancel()
        self.assertEqual(property_record.state, "canceled")

    def test_write_sets_state_offer_received_when_offer_exists(self):
        property_record = self._create_property()
        self._create_offer(property_record, price=850000.0)
        property_record.write({"state": "new"})
        self.assertEqual(property_record.state, "offer_received")

    def test_write_sets_state_back_to_new_when_no_offer(self):
        property_record = self._create_property()
        offer = self._create_offer(property_record, price=850000.0)
        offer.unlink()
        property_record.write({"state": "offer_received"})
        self.assertEqual(property_record.state, "new")

    def test_unlink_allowed_when_state_new(self):
        property_record = self._create_property()
        property_record.unlink()
        self.assertFalse(property_record.exists())

    def test_unlink_allowed_when_state_canceled(self):
        property_record = self._create_property()
        property_record.write({"state": "canceled"})
        property_record.unlink()
        self.assertFalse(property_record.exists())

    def test_unlink_blocked_when_state_sold(self):
        property_record = self._create_property()
        property_record.write({"state": "sold"})
        with self.assertRaises(UserError):
            property_record.unlink()

    def test_action_print_qweb_report_returns_report_action(self):
        property_record = self._create_property()
        action = property_record.action_print_qweb_report()
        self.assertIn(action.get("type"), {"ir.actions.report", "ir.actions.act_window"})
