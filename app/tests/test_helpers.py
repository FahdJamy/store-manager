from unittest import TestCase
from app import app
from . import base
from app.utils.helpers import string_validator


""" Test case for helpers (utils)."""


class TestHelpersCase (TestCase):  # Inherit Testcase class

    """ Should run before start of a test method"""

    def setUp(self):
        self.current_app = app

    def test_string_validator(self):
    	response = string_validator('$#@')
    	self.assertEqual('special character exists', response)
    	response = string_validator('    ')
    	self.assertIsNone(response)
    	response = string_validator('food')
    	self.assertIsNotNone(response)
    	self.assertEqual('valid', response)