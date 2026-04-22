from datetime import date, timedelta

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestEstatePropertyOffer(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.property_type = cls.env["estate.property.type"].create({
            "name": "Residential Offer Test",
        })
        cls.partner = cls.env["res.partner"].create({
            "name": "Partner Offer Test",
        })
        cls.other_partner = cls.env["res.partner"].create({
            "name": "Other Partner Offer Test",
        })

    def _create_property(self, **extra_vals):
        vals = {
            "name": "Property Offer Test",
            "expected_price": 1000000.0,
            "property_type_id": self.property_type.id,
        }
        vals.update(extra_vals)
        return self.env["estate.property"].create(vals)

    def _create_offer(self, property_record, **extra_vals):
        vals = {
            "name": "Offer Test",
            "price": 900000.0,
            "property_id": property_record.id,
            "partner_id": self.partner.id,
        }
        vals.update(extra_vals)
        return self.env["estate.property.offer"].create(vals)

    def test_create_offer_sets_property_state_offer_received_on_first_offer(self):
        property_record = self._create_property()
        self.assertEqual(property_record.state, "new")
        self._create_offer(property_record)
        self.assertEqual(property_record.state, "offer_received")

    def test_create_offer_rejects_price_lower_than_best_price(self):
        property_record = self._create_property()
        self._create_offer(property_record, price=900000.0)
        with self.assertRaises(ValidationError):
            self._create_offer(property_record, price=850000.0, partner_id=self.other_partner.id)

    def test_offer_price_constraint_rejects_zero_or_negative_price(self):
        property_record = self._create_property()
        with self.assertRaises(ValidationError):
            self._create_offer(property_record, price=0.0)

    def test_compute_date_deadline_from_validity(self):
        property_record = self._create_property()
        offer = self._create_offer(property_record, validity=10)
        self.assertEqual(offer.date_deadline, date.today() + timedelta(days=10))

    def test_inverse_date_deadline_updates_validity(self):
        property_record = self._create_property()
        offer = self._create_offer(property_record, validity=7)
        target_deadline = date.today() + timedelta(days=3)
        offer.write({"date_deadline": target_deadline})
        self.assertEqual(offer.validity, 3)

    def test_act_offer_accepted_updates_property_and_offer(self):
        property_record = self._create_property(expected_price=1000000.0)
        offer = self._create_offer(
            property_record,
            price=900000.0,
            partner_id=self.other_partner.id,
        )
        offer.act_offer_accepted()
        self.assertEqual(offer.status, "accepted")
        self.assertEqual(property_record.partner_id, self.other_partner)
        self.assertEqual(property_record.selling_price, 900000.0)

    def test_act_offer_refused_sets_offer_status_refused(self):
        property_record = self._create_property()
        offer = self._create_offer(property_record)
        offer.act_offer_refused()
        self.assertEqual(offer.status, "refused")

    def test_related_property_type_is_set_from_property(self):
        property_record = self._create_property()
        offer = self._create_offer(property_record)
        self.assertEqual(offer.property_type_id, property_record.property_type_id)
