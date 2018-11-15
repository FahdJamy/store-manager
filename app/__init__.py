import os
from flask import Flask, jsonify
from flask_restplus import Api
from app.config import config_app
from flask_cors import CORS

app = Flask(__name__)
config_name = ""
if os.getenv('CONFIG_NAME') == 'testing':
    config_name = os.getenv('TESTING_CONF')
elif os.getenv('CONFIG_NAME') == 'develop':
	config_name = os.getenv('DEVELOPMENT_CONF')
elif os.getenv('CONFIG_NAME') == 'heroku':
	config_name = os.getenv('PRODUCTION_CONF')
else:
    config_name = os.getenv('DEPLOYMENT_CONF')

app.config.from_object(config_app[config_name])
print(app.config['DATABASE'])

api = Api(app, prefix="/api/v2", version='2')
CORS(app)

from app.routes import users, categories, products, sales


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': 'Sorry the URL you are trying to access doesnot exist'}), 404


@api.errorhandler
def internal_server_error(error):
    return {'message': str(error)}, getattr(error, 'code', 500)
