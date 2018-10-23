import json
from unittest import TestCase
from app import app


class TestValidationCase(TestCase):
    def setUp(self):
        self.app = app.test_client()

    def test_product_name_value(self):
        with self.app as c:
            resp = c.post('/api/v1/products', data=json.dumps(
                {'name': 40, 'category': 'electronic', 'price': 40}), content_type='application/json')
            self.assertEqual(resp.status_code, 400)
            data = json.loads(resp.data)
            message = str(data['errors']['name'])
            self.assertEqual(message, "40 is not of type 'string'")
