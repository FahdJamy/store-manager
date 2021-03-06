import json
from unittest import TestCase
from app import app
from app.models.products import Product


""" Test case for api endpoints."""


class TestApiRoutesCase(TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.pdts_db = Product()

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

    """ Test Return a single product given it ID api endpoint  """

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

    """ Test new sales record creation. api endpoint"""

    def test_sales_record_creation(self):
        with self.app as c:
            response = c.post('/api/v1/sales', data=json.dumps(
                {'name': 'pixel', 'category': 'electronic', 'price': 40, 'quantity': 2}), content_type='application/json')
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.data)
            self.assertEqual(response_data['Sales record']['total_amount'], 80)

    """ Test retrival off all available sale record API endpoint."""

    def test_retrieve_all_sale_records(self):
        with self.app as c:
            response = c.get('/api/v1/sales')
            self.assertEqual(response.status_code, 200)

    """ Test return sale record given its ID api endpoint."""

    def test_get_sale_record_given_an_id(self):
        with self.app as c:
            response = c.get('/api/v1/sale/390')
            self.assertEqual(response.status_code, 400)
            ressp = c.post('/api/v1/sales', data=json.dumps(
                {'name': 'pixel', 'category': 'electronic', 'price': 40, 'quantity': 2}), content_type='application/json')
            self.assertEqual(201, ressp.status_code)
            resp = c.get('/api/v1/sale/1')
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
            self.assertIn("pixel", str(resp.data))
            resp_data = json.loads(resp.data)
            self.assertEqual(expected, resp_data)

    """ Test message returned on access of an invalid api endpoint """

    def test_invalid_URL(self):
        with self.app as c:
            response = c.get('/api/v1/allProducts')
            self.assertEqual(response.status_code, 404)
            data = json.loads(response.data)
            message = str(data['message'])
            self.assertEqual(
                message, 'Sorry the URL you are trying to access doesnot exist')
