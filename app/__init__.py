from flask import Flask
from app.utils.config import Config
from flask_restplus import Api

app = Flask(__name__)
app.config.from_object(Config)

api = Api(app, prefix="/api/v1",version='1')

from .routes import products, sales