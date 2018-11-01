import os
from os.path import dirname, join
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

class Config:
	DEBUG=True
	SECRET_KEY=os.getenv('SECRET_KEY') or 'c24f51ba-4a64-49be-9dbf-310041029a45'
	DATABASE='postgresql://postgres:postgres@localhost:5432/store_manager'

class ProductionConfig(Config):
	DEBUG=False
	DATABASE=os.getenv('DATABASE_URL')

class TestingConfig(Config):
	DATABASE=os.getenv('TESTING_DATABASE')

class DevelopmentConfig(Config):
	DATABASE=os.getenv('DEVELOPMENT_DATABASE')

class DeploymentConfig(Config):
	DEBUG=False

config_app = {
	"Production":ProductionConfig,
	"Testing":TestingConfig,
	"Deployment":DeploymentConfig,
	"Development":DevelopmentConfig
}