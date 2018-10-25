import json
from unittest import TestCase
from app import app


""" Test case for value validations."""


class TestValidationCase(TestCase):
    """ Run before every start of a new test method"""

    def setUp(self):
        self.app = app.test_client()

    """ Test product name input value. message and status code returned if not a string."""

    def test_product_name_value_validation(self):
        with self.app as c:
            response = c.post('/api/v1/products', data=json.dumps(
                {'name': 40, 'category': 'electronic', 'price': 40}), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            message = str(data['errors']['name'])
            self.assertEqual(message, "40 is not of type 'string'")

    """ Test product category input value. message and status code returned if not a string."""

    def test_product_category_value_validation(self):
        with self.app as c:
            response = c.post('/api/v1/products', data=json.dumps(
                {'name': 'pixel', 'category': 5000, 'price': 40}), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            message = str(data['errors']['category'])
            self.assertEqual(message, "5000 is not of type 'string'")

    """ Test product price input value. message and status code returned if value is not an integer."""

    def test_product_price_value_validation(self):
        with self.app as c:
            response = c.post('/api/v1/products', data=json.dumps(
                {'name': 'pixel', 'category': 'phone', 'price': 'sixty'}), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            message = str(data['errors']['price'])
            self.assertEqual(message, "'sixty' is not of type 'integer'")

    """ Test sales record product name and its category input values. message and status code returned if values are not strings."""

    def test_sales_product_name_and_category_value_validation(self):
        with self.app as c:
            response = c.post('/api/v1/sales', data=json.dumps(
                {'name': 200, 'category': 'electronic', 'price': 40, 'quantity': 2}), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            message = str(data['errors']['name'])
            self.assertEqual(message, "200 is not of type 'string'")

            response = c.post('/api/v1/sales', data=json.dumps(
                {'name': 'google pixel', 'category': 700.9, 'price': 40, 'quantity': 2}), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            message = str(data['errors']['category'])
            self.assertEqual(message, "700.9 is not of type 'string'")

    """ Test sales record product price input and quantity values. message and status code returned if values are not integers."""

    def test_sales_product_price_and_quantity_value_validation(self):
        with self.app as c:
            response = c.post('/api/v1/sales', data=json.dumps(
                {'name': 'google pixel',
                 'category': 'smart phone',
                 'price': 'mood',
                 'quantity': 'twenty'}),
                content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            price_message = str(data['errors']['price'])
            self.assertEqual(price_message, "'mood' is not of type 'integer'")
            quantity_message = str(data['errors']['quantity'])
            self.assertEqual(quantity_message,
                             "'twenty' is not of type 'integer'")
