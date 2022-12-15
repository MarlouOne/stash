# DATABASE_NAME = 'news.db'


from sqlalchemy.orm import sessionmaker, Session
from pprint import pprint
import inspect
from news_schema import Countries, News, get_engine


def showVarType(var) -> None: # Узнаём тип данных произвольной переменной
    caller_locals = inspect.currentframe().f_back.f_locals
    varName = [name for name, value in caller_locals.items() if var is value] # Получаем имя переменной 
    print(f'\n{varName} type is {type(var)}') # Узнаём тип данных переменной 


# engine = get_engine()
# session = Session(bind=engine)

# result = session.query(Countries.id, Countries.text, Countries.country).all().distinct()

# showVarType(result)
# pprint(result)

# session.delete(result) # Удаляем из таблици полученные строки

# result = list(set(result))  # Удаление дубликатов

# pprint(result)


# session.add(result)
# session.commit()