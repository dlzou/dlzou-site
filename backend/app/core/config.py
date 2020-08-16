from starlette.config import Config

config = Config('.env')

PROJECT_NAME = config('PROJECT_NAME', default='FastAPI application')
API_PATH = config('API_PATH', default='')
SQLALCHEMY_DB_URL = config('SQLALCHEMY_DB_URL', default='sqlite:///./content.db')

SECRET_KEY = config('SECRET_KEY', default='')
ACCESS_TOKEN_EXPIRE_MIN = config('ACCESS_TOKEN_EXPIRE_MIN', default=60)
SLUG_LEN = config('SLUG_LEN', default=30)
