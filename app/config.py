import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
	DEBUG=False
	SECRET_KEY=os.getenv('SECRET_KEY') or 'c24f51ba-4a64-49be-9dbf-310041029a45'
	DATABASE='postgresql://postgres:postgres@localhost:5432/store_manager'

class ProductionConfig(Config):
	DEBUG=True
	DATABASE=os.getenv('PRODUCTION_DATABASE')

class TestingConfig(Config):
	DEBUG=True
	DATABASE=os.getenv('TESTING_DATABASE')

class DeploymentConfig(Config):
	DEBUG=False

config_app = {
	"Production":ProductionConfig,
	"Testing":TestingConfig,
	"Deployment":DeploymentConfig
}