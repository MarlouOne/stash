from sqlalchemy import create_engine, INTEGER, \
    Column, VARCHAR, DATE, PrimaryKeyConstraint, DateTime, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime

import re
from pprint import pprint



Base = declarative_base()

class Countries(Base):
    __tablename__ = 'countries'
    id = Column(INTEGER)
    text = Column(VARCHAR(length=255), nullable=False)
    country = Column(VARCHAR(length=255), nullable=False)
    date = Date
    __table_args__ = (
        PrimaryKeyConstraint('id', name='id'),
    )

class News(Base):
    __tablename__ = 'news'
    id = Column(INTEGER)
    title = Column(VARCHAR(length=255), nullable=False)
    href = Column(VARCHAR(length=255), nullable=False)
    date = Date
    __table_args__ = (
        PrimaryKeyConstraint('id', name='id'),
    )

def get_engine():
    DATABASE_NAME = 'news.db'
    engine = create_engine(f'sqlite:///{DATABASE_NAME}')
    base = Base.metadata.create_all(engine)

    return engine

def main():
    session = Session(bind=get_engine())
    pprint(session.query(Countries.id, Countries.text).all())


if __name__ == '__main__': # Если файл tg_bot.py вызаван, то будет запущен main(strBotToken); Если он будет импортироват то ничего не произайдёт
    main()

print(f'{__name__} is here !')