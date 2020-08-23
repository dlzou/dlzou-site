from starlette.config import Config

config = Config('.env')

PROJECT_NAME = config('PROJECT_NAME', default='FastAPI application')
API_PATH = config('API_PATH', default='')
SQLALCHEMY_DB_URL = config('SQLALCHEMY_DB_URL', default='sqlite:///./content.db')
SLUG_LEN = config('SLUG_LEN', default=30)

SECRET_KEY = config('SECRET_KEY', default='')  # generate with openssl rand -hex 32
ACCESS_TOKEN_EXPIRE_MIN = config('ACCESS_TOKEN_EXPIRE_MIN', default=60)
JWT_SIGN_ALGORITHM = config('JWT_SIGN_ALGORITHM', default='HS256')
