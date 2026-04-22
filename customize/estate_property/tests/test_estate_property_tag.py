from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase


class TestEstatePropertyTag(TransactionCase):
    def test_create_tag_success(self):
        tag = self.env["estate.property.tag"].create({
            "name": "Premium",
            "color": 3,
        })
        self.assertTrue(tag.exists())
        self.assertEqual(tag.name, "Premium")
        self.assertEqual(tag.color, 3)

    def test_tag_name_must_be_unique(self):
        self.env["estate.property.tag"].create({"name": "Duplicate Name"})
        with self.assertRaises(Exception) as ctx:
            self.env["estate.property.tag"].create({"name": "Duplicate Name"})
        self.assertIsInstance(ctx.exception, (ValidationError, IntegrityError))

    def test_tag_name_is_required(self):
        with self.assertRaises(Exception) as ctx:
            self.env["estate.property.tag"].create({"color": 5})
        self.assertIsInstance(ctx.exception, (ValidationError, IntegrityError))
