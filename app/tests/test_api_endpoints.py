import json
from unittest import TestCase
from app import app
from app.models.products import Products


class TestApiRoutesCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.pdts_db = Products()
        self.pdts_db.delete_products()

    """ Test product creation endpoint """
    def test_api_product_creation(self):
        with self.app as c:
            response = c.post('/api/v1/products')
            self.assertEqual(response.status_code, 400)
            resp = c.post('/api/v1/products', data=json.dumps(
                {'name': 'pixel', 'category': 'electronic', 'price': 40}), content_type='application/json')
            self.assertEqual(resp.status_code, 201)