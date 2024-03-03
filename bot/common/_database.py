from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ._config import settings

engine = create_engine(
    url = settings.DATABASE_URI
)

session = Session(bind=engine)


