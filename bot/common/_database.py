from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from ._config import settings

#подключение к базе данных 
engine = create_engine(
    url = settings.DATABASE_URI
)

#создания сессии для взаимодействия с базой данных 
session = Session(bind=engine)


