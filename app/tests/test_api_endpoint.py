import json
from datetime import datetime
from unittest import TestCase
from app import app
from . import base
from app.utils.helpers import generate_token
from app.db.db import DB
from app.db.users import User


""" Test case for api endpoints."""


class TestApiEndpointsCase (TestCase):  # Inherit from Testcase class

    """ Should run before start of a test method"""

    def setUp(self):
        self.current_app = app
        with self.current_app.app_context():
            self.db = DB()
            self.usr = User()
        self.usr.create_user('Admin', '123')
        self.usr.update_user_info(1, True)
        self.client = app.test_client()
        self.user = {'username': 'me', 'password': '123'}
        self.date = str((datetime.utcnow()).strftime('%d %b,%Y'))
        self.new_category = {'name': 'food',
                             'description': 'this is the best category'}
        self.update_category_info = {'name': 'moon',
                                     'description': 'this is the best category'}
        self.new_product = {'name': 'maize',
                            'category': 'food',
                            'price': 80,
                            'quantity': 37}
        self.sale_record = {
            'name': 'maize',
            'quantity': 7
        }
        self.update_product_info = {
            'name': 'maize floor', 'price': 80, 'quantity': 37}
        self.token = generate_token('Admin')
        self.usr.create_user('Wow', '123')
        self.attendant_token = generate_token('Wow')

    """ Test new sales attendant account creation by admin only"""

    def test_user_signup_api_endpoint(self):
        with self.client as c:
            response = c.post('/api/v2/auth/signup')
            self.assertEqual(response.status_code, 400)
            response = c.post(
                '/api/v2/auth/signup', data=json.dumps(self.user), content_type='application/json')
            self.assertEqual(response.status_code, 401)
            response = c.post('/api/v2/auth/signup', data=json.dumps(self.user), headers={
                              'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(str(json.loads(response.data)),
                             "{'message': 'User succefully registered'}")

    """ Test user login api endpoint"""

    def test_user_login_api_endpoint(self):
        with self.client as c:
            response = c.post(
                '/api/v2/auth/login', data=json.dumps(self.user), content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(str(json.loads(
                response.data)), "{'message': 'Sorry user Me doesnot exist, login with valid credentials'}")
            c.post('/api/v2/auth/signup', data=json.dumps(self.user), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.post(
                '/api/v2/auth/login', data=json.dumps(self.user), content_type='application/json')
            self.assertEqual(response.status_code, 200)

    """ Test giving admin right to sales attendant"""

    def test_promote_sales_attendant_to_admin(self):
        with self.client as c:
            response = c.put(
                '/api/v2/user/1', data=json.dumps(self.user), content_type='application/json')
            self.assertEqual(response.status_code, 401)
            self.assertEqual(str(json.loads(response.data)),
                             "{'message': 'sorry, you missing a token'}")
            c.post('/api/v2/auth/signup', data=json.dumps(self.user),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.put('/api/v2/user/1', data=json.dumps({'admin': True}), headers={
                             'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(str(json.loads(response.data)),
                             "{'message': 'user has been promoted to an admin'}")

    """ Test category creation"""

    def test_new_category_creation(self):
        with self.client as c:
            response = c.get('/api/v2/categories/all')
            self.assertEqual(response.status_code, 404)
            response = c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                              'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(str(json.loads(
                response.data)), "{'message': 'category has been successfully created !!!'}")

    """ Test get all categories"""

    def test_get_all_categories(self):
        with self.client as c:
            response = c.get('/api/v2/categories')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(str(json.loads(
                response.data)), "{'message': 'sorry, no categories exist in the database'}")
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.get('/api/v2/categories')
            self.assertEqual(response.status_code, 200)
            expected = {'categories': [
                {'id': 1, 'category_name': 'Food', 'description': 'this is the best category'}]}
            self.assertEqual((json.loads(response.data)), expected)

    """ Test get category by Id"""

    def test_get_category_by_Id(self):
        with self.client as c:
            response = c.get('/api/v2/category/1')
            self.assertEqual(response.status_code, 400)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry category with id 1 does not exist'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.get('/api/v2/category/1')
            self.assertEqual(response.status_code, 200)
            expected = {'category': {'category_name': 'Food',
                                     'description': 'this is the best category',
                                     'id': 1}}
            self.assertEqual((json.loads(response.data)), expected)

    """ Test get specific category given Id"""

    def test_delete_category_by_Id(self):
        with self.client as c:
            response = c.delete('/api/v2/category/1')
            self.assertEqual(response.status_code, 401)
            self.assertEqual(json.loads(response.data), {
                             'message': 'sorry, you missing a token'})
            response = c.delete('/api/v2/category/1', headers={
                'token_key': '{}'.format(self.token)})
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry category with Id 1 doesnot exist'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.delete('/api/v2/category/1', headers={
                'token_key': '{}'.format(self.token)})
            self.assertEqual(response.status_code, 200)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'category with Id 1 has been deleted'})

    """ Test update category information"""

    def test_update_category_info_by_Id(self):
        with self.client as c:
            response = c.put('/api/v2/category/1', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry category with Id 1 does not exist'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.put('/api/v2/category/1', data=json.dumps(self.update_category_info), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(response.status_code, 200)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'category info successfully updated'})

    """ Test new product creation by admin only"""

    def test_new_product_creation(self):
        with self.client as c:
            response = c.post('/api/v2/products')
            self.assertEqual(response.status_code, 400)
            response = c.post(
                '/api/v2/products', data=json.dumps(self.new_product), content_type='application/json')
            self.assertEqual(response.status_code, 401)
            self.assertEqual((json.loads(
                response.data)), {'message': 'sorry, you missing a token'})
            response = c.post('/api/v2/products', data=json.dumps(self.new_product), headers={
                              'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(json.loads(
                response.data), {'message': 'category name Food doesnot exist'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.post('/api/v2/products', data=json.dumps(self.new_product), headers={
                              'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(json.loads(
                response.data), {'message': 'product has been created successfully!!!'})

    """ Test get all available products api Endpoint"""

    def test_get_all_products(self):
        with self.client as c:
            response = c.get('/api/v2/products')
            self.assertEqual(response.status_code, 400)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry no products exist yet'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/products', data=json.dumps(self.new_product),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.get('/api/v2/products')
            self.assertEqual(response.status_code, 200)
            expected = {'Products': [{'category': 'Food',
                                      'id': 1,
                                      'price': 80,
                                      'product_name': 'Maize',
                                      'stock': 37}]}
            self.assertEqual((json.loads(response.data)), expected)

    """ Test get a specific product by its Id"""

    def test_get_product_by_Id(self):
        with self.client as c:
            response = c.get('/api/v2/products/1')
            self.assertEqual(response.status_code, 400)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry product with id 1 does not exist'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/products', data=json.dumps(self.new_product),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.get('/api/v2/products/1')
            self.assertEqual(response.status_code, 200)
            expected = {'product': {'id': 1,
                                    'product_name': 'Maize',
                                    'category': 'Food',
                                    'price': 80,
                                    'stock': 37
                                    }}
            self.assertEqual((json.loads(response.data)), expected)

    """ Test delete a product by its Id. (Endpoint accessed to only admin)"""

    def test_delete_product_by_Id(self):
        with self.client as c:
            response = c.delete('/api/v2/products/1')
            self.assertEqual(response.status_code, 401)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry, you missing a token'})
            response = c.delete('/api/v2/products/1',
                                headers={'token_key': '{}'.format(self.token)})
            self.assertEqual(response.status_code, 400)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry product with Id 1 doesnot exist'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/products', data=json.dumps(self.new_product),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.delete('/api/v2/products/1',
                                headers={'token_key': '{}'.format(self.token)})
            self.assertEqual(response.status_code, 200)

    """ Test update product api endpoint"""

    def test_update_product_info(self):
        with self.client as c:
            response = c.put('/api/v2/products/1')
            self.assertEqual(response.status_code, 401)
            response = c.put('/api/v2/products/1', data=json.dumps(
                self.update_product_info), headers={'token_key': '{}'.format(self.token)})
            self.assertEqual(response.status_code, 400)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry product with Id 1 does not exist'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/products', data=json.dumps(self.new_product),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.put('/api/v2/products/1', data=json.dumps(self.update_product_info),
                             headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual((json.loads(response.data)), {
                             'message': 'product info successfully updated'})

    """ Tets create new sale record."""

    def test_create_new_sales_record(self):
        with self.client as c:
            response = c.post('/api/v2/sales', data=json.dumps(self.sale_record), headers={
                              'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(response.status_code, 401)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry an admin cant create a sales record'})
            response = c.post('/api/v2/sales', data=json.dumps(self.sale_record), headers={
                              'token_key': '{}'.format(self.attendant_token)}, content_type='application/json')
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry cant make a sale record of a product that doesnt exist in the db'})
            self.assertEqual(response.status_code, 400)
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/products', data=json.dumps(self.new_product),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            response = c.post('/api/v2/sales', data=json.dumps(self.sale_record), headers={
                              'token_key': '{}'.format(self.attendant_token)}, content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sale record created'})

    """ Test get all sales records."""

    def test_get_sales_records(self):
        with self.client as c:
            response = c.get(
                '/api/v2/sales', headers={'token_key': '{}'.format(self.token)})
            self.assertEqual(response.status_code, 400)
            self.assertEqual((json.loads(response.data)), {
                             'sales': 'sorry no sales records exist in the db yet'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/products', data=json.dumps(self.new_product),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/sales', data=json.dumps(self.sale_record), headers={
                   'token_key': '{}'.format(self.attendant_token)}, content_type='application/json')
            response = c.get(
                '/api/v2/sales', headers={'token_key': '{}'.format(self.token)})
            self.assertEqual(response.status_code, 200)
            expected = {'sales': [
                {'category': 'Food',
                 'created_by': 'Wow',
                 'created_on': self.date,
                 'id': 1,
                 'price': 80,
                 'product_name': 'Maize',
                 'quantity': 7,
                 'total_amount': 560}]}
            self.assertEqual((json.loads(response.data)), expected)

    """ Tets get specific sale record by Id."""

    def test_get_specific_sale_record_given_Id(self):
        with self.client as c:
            response = c.get(
                '/api/v2/sales/1', headers={'token_key': '{}'.format(self.token)})
            self.assertEqual(response.status_code, 400)
            self.assertEqual((json.loads(response.data)), {
                             'sale record': 'sorry, sale record of id 1 doesnot exists'})
            c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/products', data=json.dumps(self.new_product),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/sales', data=json.dumps(self.sale_record), headers={
                   'token_key': '{}'.format(self.attendant_token)}, content_type='application/json')
            response = c.get(
                '/api/v2/sales/1', headers={'token_key': '{}'.format(self.token)})
            self.assertEqual(response.status_code, 200)
            expected = {'sale record':
                        {'category': 'Food',
                         'created_by': 'Wow',
                         'created_on': self.date,
                         'id': 1,
                         'price': 80,
                         'product_name': 'Maize',
                         'quantity': 7,
                         'total_amount': 560}}
            self.assertEqual((json.loads(response.data)), expected)

    """ Test delete specific category by Id."""

    def test_delete_sale_record_by_Id(self):
        with self.client as c:
            response = c.delete(
                '/api/v2/sales/1', headers={'token_key': '{}'.format(self.attendant_token)})
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sorry u not an admin, u cant access this endpoint'})
            c.post('/api/v2/products', data=json.dumps(self.new_product),
                   headers={'token_key': '{}'.format(self.token)}, content_type='application/json')
            c.post('/api/v2/sales', data=json.dumps(self.sale_record), headers={
                   'token_key': '{}'.format(self.attendant_token)}, content_type='application/json')
            response = c.delete(
                '/api/v2/sales/1', headers={'token_key': '{}'.format(self.token)})
            self.assertEqual((json.loads(response.data)), {
                             'message': 'sale record has been deleted'})
            self.assertEqual(response.status_code, 200)

    def tearDown(self):
        self.db.drop_tables('users', 'sales', 'products', 'categories')
