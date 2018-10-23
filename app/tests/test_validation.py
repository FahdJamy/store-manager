import json
from unittest import TestCase
from app import app


class TestValidationCase(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_product_name_value_validation(self):
        with self.app as c:
            response = c.post('/api/v1/products', data=json.dumps(
                {'name': 40, 'category': 'electronic', 'price': 40}), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            message = str(data['errors']['name'])
            self.assertEqual(message, "40 is not of type 'string'")

    def test_product_category_value_validation(self):
        with self.app as c:
            response = c.post('/api/v1/products', data=json.dumps(
                {'name': 'pixel', 'category': 5000, 'price': 40}), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            message = str(data['errors']['category'])
            self.assertEqual(message, "5000 is not of type 'string'")

    def test_product_price_value_validation(self):
        with self.app as c:
            response = c.post('/api/v1/products', data=json.dumps(
                {'name': 'pixel', 'category': 'phone', 'price': 'sixty'}), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            data = json.loads(response.data)
            message = str(data['errors']['price'])
            self.assertEqual(message, "'sixty' is not of type 'integer'")

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
