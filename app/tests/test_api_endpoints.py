import json
from unittest import TestCase
from app import app
from app.models.products import Products


class TestApiRoutesCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.pdts_db = Products()

    """ Test product creation endpoint """

    def test_api_product_creation(self):
        with self.app as c:
            response = c.post('/api/v1/products')
            self.assertEqual(response.status_code, 400)
            resp = c.post('/api/v1/products', data=json.dumps(
                {'name': 'pixel', 'category': 'electronic', 'price': 40}), content_type='application/json')
            self.assertEqual(resp.status_code, 201)

    """ Test get all products endpoint """

    def test_get_all_products(self):
        with self.app as c:
            response = c.get('/api/v1/products')
            self.assertEqual(response.status_code, 200)

    def test_get_a_product_by_id(self):
        with self.app as c:
            response = c.get('/api/v1/products/4')
            self.assertEqual(response.status_code, 400)
            resp = c.post('/api/v1/products', data=json.dumps(
                {'name': 'pixel', 'category': 'electronic', 'price': 40}), content_type='application/json')
            responseAfterPdtCreation = c.get('/api/v1/products/1')
            print(responseAfterPdtCreation)
            self.assertIsNotNone(responseAfterPdtCreation)
            expected = json.loads(responseAfterPdtCreation.data)
            self.assertEqual('pixel', expected['name'])

    def test_sales_record_creation(self):
        with self.app as c:
            response = c.post('/api/v1/sales', data=json.dumps(
                {'name': 'pixel', 'category': 'electronic', 'price': 40, 'quantity': 2}), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['Sales record']['total_amount'], 80)

    def test_retrieve_all_sale_records(self):
        with self.app as c:
            response = c.get('/api/v1/sales')
            self.assertEqual(response.status_code, 200)

    def test_get_sale_record_given_an_id(self):
        with self.app as c:
            response = c.get('/api/v1/sales/390')
            self.assertEqual(response.status_code, 400)
            resp = c.post('/api/v1/sales', data=json.dumps(
                {'name': 'pixel', 'category': 'electronic', 'price': 40, 'quantity': 2}), content_type='application/json')
            expected = {
                "id": 1,
                "product_name": "pixel",
                "price": 40,
                "category": "electronic",
                "quantity": 2,
                "total_amount": 80,
                "created_by": "mags"
            }
            self.assertEqual(resp.status_code, 200)
            resp_data = json.loads(resp.data)
            self.assertDictEqual(expected, resp_data)
