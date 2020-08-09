from starlette.config import Config

config = Config('.env')

PROJECT_NAME = config('PROJECT_NAME', default='FastAPI application')
API_PATH = config('API_PATH', default='')
SQLALCHEMY_DB_URL = config('SQLALCHEMY_DB_URL', default='sqlite:///./content.db')
