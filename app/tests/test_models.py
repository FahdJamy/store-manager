from unittest import TestCase
from app.models.products import Products


class TestModelCase (TestCase):

    """ Should be run before start of a test method"""

    def setUp(self):
        self.pdt_model = Products()

    """ tests for new product creation """

    def test_product_creation(self):
        # check wether product of id 1 exists
        result = self.pdt_model.find_product_by_id(1)
        self.assertIsNone(result)
        self.assertRaises(
            TypeError, self.pdt_model.find_product_by_id, 9, "wee")
        # Create user
        result = self.pdt_model.create_new_product('timberland', 'shoe', 90)
        self.assertIsNotNone(result)
        expected = {
            "id": 1,
            "name": 'timberland',
            "price": 90,
            "category": 'shoe'
        }
        self.assertDictEqual(result, expected)
        self.assertEqual(result['id'], 1)
