import os
from dotenv import find_dotenv, load_dotenv
from sqlalchemy import create_engine
from database.models import Base


load_dotenv(find_dotenv())


def get_engine():
    return create_engine(
        f"postgresql+psycopg2://{os.getenv('PG_USER')}:{os.getenv('PG_PASSWORD')}"
        f"@{os.getenv('PG_HOST')}:{os.getenv('PG_PORT')}/{os.getenv('PG_DB')}", pool_pre_ping=True)


def create_db():
    Base.metadata.create_all(get_engine())


def delete_db():
    Base.metadata.drop_all(get_engine())


create_db()