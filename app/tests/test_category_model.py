from unittest import TestCase
from app import app
from . import base
from app.db.categories import Category
from app.db.db import DB


""" Test case for category model."""


class TestModelsCase (TestCase):  # Inherit Testcase class

    """ Should run before start of a test method"""

    def setUp(self):
        self.current_app = app
        with self.current_app.app_context():
            self.db = DB()
            self.categ_model = Category()

    """ Test creation of a new category."""

    def test_category_creation(self):
        response = self.categ_model.create_category(
            'Food', 'This should only be foods')
        self.assertIsNotNone(response)
        self.assertEqual('category created successfully', response)
        self.assertRaises(
            TypeError, self.categ_model.find_category_by_name, 2, "main")

    def test_find_category_by_name(self):
        response = self.categ_model.find_category_by_name('food')
        self.assertEqual('no result found', response)
        self.categ_model.create_category('food', 'This should only be foods')
        response = self.categ_model.find_category_by_name('food')
        expected = {'id': 1, 'category_name': 'food', 'description': 'This should only be foods'}
        self.assertEqual(expected, response)

    def test_delete_category_by_Id(self):
        response = self.categ_model.delete_category_by_Id(1)
        self.assertIsNone(response)
        self.categ_model.create_category('food', 'This should only be foods')
        response = self.categ_model.delete_category_by_Id(1)
        self.assertIsNotNone(response)
        self.assertEqual(response, 'category deleted')

    def test_category_given_Id(self):
        response = self.categ_model.return_category_info_given_Id(1)
        self.assertIsNone(response)
        self.categ_model.create_category('food', 'This should only be foods')
        response = self.categ_model.return_category_info_given_Id(1)
        self.assertIsNotNone(response)
        expected = {'id': 1,
                    'category_name': 'food',
                    'description': 'This should only be foods'}
        self.assertEqual(expected, response)

    def test_update_category_info(self):
        response = self.categ_model.update_category(1, 'Weed', 'weed is a great herb')
        self.assertIsNone(response)
        self.categ_model.create_category('food', 'This should only be foods')
        response = self.categ_model.update_category(1, 'Weed', 'weed is a great herb')
        self.assertIsNotNone(response)
        self.assertEqual('category info successfully updated', response)

    def test_get_all_categories(self):
        response = self.categ_model.get_all_available_categories()
        self.assertIsNone(response)
        self.categ_model.create_category('food', 'This should only be foods')
        response = self.categ_model.get_all_available_categories()
        self.assertIsNotNone(response)
        self.assertEqual(response, [{'id': 1, 'category_name': 'food', 'description': 'This should only be foods'}])

    def tearDown(self):
        self.db.drop_tables('users', 'sales', 'products', 'categories')
