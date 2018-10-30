from . import base
import json
from unittest import TestCase
from app import app
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
        self.token = generate_token('Admin')

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

    def test_new_category_creation(self):
        with self.client as c:
            response = c.get('/api/v2/categories/all')
            self.assertEqual(response.status_code, 404)
            response = c.post('/api/v2/categories', data=json.dumps(self.new_category), headers={
                              'token_key': '{}'.format(self.token)}, content_type='application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(str(json.loads(
                response.data)), "{'message': 'category has been successfully created !!!'}")

    def tearDown(self):
        self.db.drop_tables('users', 'sales', 'products', 'categories')
