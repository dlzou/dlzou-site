from starlette.config import Config

config = Config('.env')

PROJECT_NAME = config('PROJECT_NAME', default='FastAPI application')
SQLALCHEMY_DB_URL = config('SQLALCHEMY_DB_URL', default='sqlite:///./sql_app.db')
