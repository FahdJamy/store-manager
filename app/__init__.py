from flask import Flask, jsonify
from app.utils.config import Config
from flask_restplus import Api

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app, prefix="/api/v1", version='1')

from .routes import products, sales


@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'message': 'Sorry the URL you are trying to access doesnot exist'}), 404


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({'message': 'Sorry we are experiencing some difficulties right now, please try again later'}), getattr(error, 'code', 500)

