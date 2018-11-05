from unittest import TestCase
from app import app
from . import base
from app.db.users import User
from app.db.db import DB


""" Test case for user model."""


class TestModelsCase (TestCase):  # Inherit Testcase class

    """ Should run before start of a test method"""

    def setUp(self):
        self.current_app = app
        with self.current_app.app_context():
            self.db = DB()
            self.user_model = User()

    """ Test registration of a User."""

    def test_user_creation(self):
        response = self.user_model.create_user("Bolly", "123Bit", 78909989)
        self.assertEqual('success', response)
        # Registration of a username that already exists
        response2 = self.user_model.create_user("Bolly", "Hennesy", 78909989)
        self.assertEqual('sorry username Bolly is already taken', response2)

    """ Test find user by Id."""

    def test_find_user_by_Id(self):
        response = self.user_model.find_user_by_Id(1)
        self.assertEqual('no result found', response)
        self.user_model.create_user("Hugs", "123Bit", 78909989)
        response = self.user_model.find_user_by_Id(1)
        expected_response = {'id': 1, 'username': 'Hugs',
                             'password': '123Bit', 'admin': False, 'phone' : 78909989}
        self.assertIsNotNone(response)
        self.assertEqual(response, expected_response)

    """ Test find user by username. """

    def test_find_user_by_username(self):
        response = self.user_model.find_user_by_username('Hugs')
        self.assertEqual('no result found', response)
        self.user_model.create_user("Hugs", "123Bit", 78909989)
        response = self.user_model.find_user_by_username('Hugs')
        expected_response = {'id': 1, 'username': 'Hugs',
                             'password': '123Bit', 'admin': False, 'phone' : 78909989}
        self.assertIsNotNone(response)
        self.assertEqual(response, expected_response)
        self.assertIn('username', response)

    """ Test get all users."""

    def test_get_all_available_users(self):
        response = self.user_model.get_all_users()
        self.assertIsNone(response)
        self.user_model.create_user("Hugs", "123Bit", 78909989)
        self.user_model.create_user("lugs", "123Bit", 78909989)
        response = self.user_model.get_all_users()
        self.assertIsNotNone(response)
        expected = [
                    {
                        'admin': False, 
                        'id': 1, 
                        'password': '123Bit', 
                        'username': 'Hugs',
                        'phone': 78909989
                        }, 
                    {
                        'admin': False, 
                        'id': 2, 
                        'password': '123Bit', 
                        'username': 'lugs',
                        'phone' : 78909989
                    }
                    ]
        self.assertEqual(response, expected)
        self.assertIn('username', response[0])
        self.assertIn('Hugs', response[0]['username'])

    """ This should run at the end of execution of a test function."""

    def test_update_user_info(self):
        self.user_model.create_user("Bolly", "123Bit", 78909989)  # Create a user first.
        response = self.user_model.update_user_info(1, True)
        self.assertRaises(
            TypeError, self.user_model.update_user_info, 1, "Billow", 90, 89)
        self.assertIsNotNone(response)
        self.assertEqual(response, 'success')
        response2 = self.user_model.update_user_info(4, True)
        self.assertEqual(response2, 'user with id 4 is not found')

    def tearDown(self):
        self.db.drop_tables('users', 'sales', 'products', 'categories')
