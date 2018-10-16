import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config ():
	SECRET_KEY = os.getenv('SECRET_KEY') or '8ffb275e274afe8cfb8d6e62573e4a'
	DEBUG = True