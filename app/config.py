import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
	DEBUG=True
	SECRET_KEY=os.getenv('SECRET_KEY') or 'c24f51ba-4a64-49be-9dbf-310041029a45'
	DATABASE_URL='postgresql://postgres:postgres@localhost:5432/store_manager'

class ProductionConfig(Config):
	DEBUG=False
	DATABASE_URL=os.getenv('PRODUCTION_DATABASE')

class TestingConfig(Config):
	DATABASE_URL=os.getenv('TESTING_DATABASE')

class DevelopmentConfig(Config):
	DATABASE_URL=os.getenv('DEVELOPMENT_DATABASE')

class DeploymentConfig(Config):
	DEBUG=False

config_app = {
	"Production":ProductionConfig,
	"Testing":TestingConfig,
	"Deployment":DeploymentConfig,
	"Development":DevelopmentConfig
}