# DATABASE_NAME = 'news.db'

import sqlalchemy 

from sqlalchemy.orm import sessionmaker, Session
from pprint import pprint
import inspect
from news_schema import Countries, News, get_engine


def showVarType(var) -> None: # Узнаём тип данных произвольной переменной
    caller_locals = inspect.currentframe().f_back.f_locals
    varName = [name for name, value in caller_locals.items() if var is value] # Получаем имя переменной 
    print(f'\n{varName} type is {type(var)}') # Узнаём тип данных переменной 


engine = get_engine()
session = Session(bind=engine)



def drop_duplicate(engine) -> None: # Удаление дубликатов из базы данных
    session = Session(bind=engine)
    #  Create a query that identifies the row for each domain with the lowest id
    inner_q = session.query(sqlalchemy.func.min(Countries.id)).group_by(Countries.text)
    aliased = sqlalchemy.alias(inner_q)
    # Select the rows that do not match the subquery
    q = session.query(Countries).filter(~Countries.id.in_(aliased))
    # Delete the unmatched rows (SQLAlchemy generates a single DELETE statement from this loop)
    for domain in q:
        session.delete(domain)
        session.commit()


    


# result = session.query(Countries.id, Countries.text, Countries.country).all()

# showVarType(result)
# pprint(result)

# session.delete(result) # Удаляем из таблици полученные строки

# result = list(set(result))  # Удаление дубликатов

# pprint(result)
# print(len(result))


# session.add(result)
# session.commit()