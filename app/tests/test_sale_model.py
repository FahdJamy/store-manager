from unittest import TestCase
from . import base
from app import app
from app.db.categories import Category
from app.db.products import Product
from app.db.sales import Sale
from app.db.db import DB
from datetime import datetime


""" Test case for sale model."""


class TestSalesModelCase (TestCase):  # Inherit from Testcase class

    """ Should run before start of a test method"""

    def setUp(self):
        self.current_app = app
        self.date = str((datetime.utcnow()).strftime('%d %b,%Y'))
        with self.current_app.app_context():
            self.db = DB()
            self.categ_model = Category()
            self.product_model = Product()
            self.sale_model = Sale()

    """ Test creation of a new sales record."""

    def test_sales_creation(self):
    	response = self.sale_model.create_sales_record('Cow', 30, 'me')
    	self.assertIsNone(response)
    	self.categ_model.create_category('Animal', 'This should only be foods')
    	self.product_model.create_product('Cow', 'Animal', 300, 11)
    	response = self.sale_model.create_sales_record('Cow', 30, 'me')
    	self.assertEqual(response, 'cant make sale, current_stock is less than provided quantity')
    	response = self.sale_model.create_sales_record('Cow', 5, 'me')
    	self.assertEqual(response, 'success')

    """ Test find sales record by Id."""

    def test_find_sale_record_by_Id(self):
    	response = self.sale_model.find_sale_by_Id(1)
    	self.assertEqual(response, 'no result found')
    	self.categ_model.create_category('Animal', 'This should only be animals')
    	self.product_model.create_product('Cow', 'Animal', 300, 11)
    	self.sale_model.create_sales_record('Cow', 5, 'me')
    	response = self.sale_model.find_sale_by_Id(1)
    	expected_response = {
	    						'id': 1, 
	    						'product_name': 'Cow', 
	    						'category': 'Animal', 
	    						'price': 300, 
	    						'quantity': 5, 
	    						'total_amount': 1500,
	    						'created_by': 'me',
	    						'created_on': self.date
    						}
    	self.assertEqual(response, expected_response)

    def tearDown(self):
        self.db.drop_tables('users', 'sales', 'products', 'categories')