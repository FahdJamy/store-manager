from unittest import TestCase
from . import base
from app import app
from app.db.products import Product
from app.db.categories import Category
from app.db.db import DB


""" Test case for product model."""


class TestProductModelsCase (TestCase):  # Inherit from Testcase class

    """ Should run before start of a test method"""

    def setUp(self):
        self.current_app = app
        with self.current_app.app_context():
            self.db = DB()
            self.product_model = Product()
            self.categ_model = Category()

    """ Test creation of a new product."""

    def test_product_creation(self):
    	response = self.product_model.create_product('casava', 'Food', 300, 11)
    	self.assertEqual(response, 'category name Food doesnot exist')
    	self.categ_model.create_category('Food', 'This should only be foods')
    	response = self.product_model.create_product('casava', 'Food', 300, 11)
    	self.assertEqual('product created successfully', response)
    	self.assertRaises(TypeError, self.product_model.create_product, 2, "main")

    """ Test update product info"""

    def test_update_product_info(self):
    	data = {
    			'name':'weed',
    			'price':20,
    			'quantity':2
    			}
    	response = self.product_model.update_product_info(1, data)
    	self.assertEqual(response, 'wrong id')
    	self.categ_model.create_category('Food', 'This should only be foods')
    	self.product_model.create_product('casava', 'Food', 300, 11)
    	response = self.product_model.update_product_info(1, data)
    	self.assertEqual(response, 'product info updated')

    """ Test delete product given ID"""

    def test_delete_product(self):
    	response = self.product_model.delete_product(1)
    	self.assertIsNone(response)
    	self.categ_model.create_category('Food', 'This should only be foods')
    	self.product_model.create_product('casava', 'Food', 300, 11)
    	response = self.product_model.delete_product(1)
    	self.assertIsNotNone(response)
    	self.assertEqual(response, 'success')

    """ Test find product by name"""

    def test_find_product_by_name(self):
    	response = self.product_model.find_product_by_name('Weed')
    	self.assertEqual(response, 'no result found')
    	self.categ_model.create_category('Food', 'This should only be foods')
    	self.product_model.create_product('Weed', 'Food', 300, 11)
    	response = self.product_model.find_product_by_name('Weed')
    	expected = {
	    				'id': 1, 
	    				'product_name': 'Weed', 
	    				'category': 'Food', 
	    				'price': 300, 
	    				'stock': 11
    				}
    	self.assertEqual(response, expected)

    """ Test find product by ID."""

    def test_find_product_by_Id(self):
    	response = self.product_model.find_product_by_Id(1)
    	self.assertEqual(response, 'no result found')
    	expected = {
	    				'id': 1, 
	    				'product_name': 'Weed', 
	    				'category': 'Food', 
	    				'price': 300, 
	    				'stock': 11
    				}
    	self.categ_model.create_category('Food', 'This should only be foods')
    	self.product_model.create_product('Weed', 'Food', 300, 11)
    	response = self.product_model.find_product_by_Id(1)
    	self.assertIsNotNone(response)
    	self.assertEqual(response, expected)


    def tearDown(self):
        self.db.drop_tables('users', 'sales', 'products', 'categories')
