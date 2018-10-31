import os
from flask import Flask
from flask_restplus import Api
from app.config import config_app

app = Flask(__name__)
config_name = ""
if os.getenv('CONFIG_NAME') == 'production':
	config_name = os.getenv('PRODUCTION_CONF')
elif os.getenv('CONFIG_NAME') == 'testing':
	config_name = os.getenv('TESTING_CONF')
elif os.getenv('CONFIG_NAME') == 'deployment':
	config_name = os.getenv('DEPLOYMENT_CONF')

app.config.from_object(config_app[config_name])
print(app.config['DATABASE'])

api = Api(app, prefix="/api/v2", version='2')

from app.routes import users, categories, products
