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

    def tearDown(self):
        self.db.drop_tables('users', 'sales', 'products', 'categories')
