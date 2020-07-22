from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core import config


engine = create_engine(config.SQLALCHEMY_DB_URL, pool_pre_ping=True)
SessionFactory = sessionmaker(bind=engine)
