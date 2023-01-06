import sqlite3

import sys, os
sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем для получения содержимого папки Google_sheets_extension

import json_handler

class sqlite_handler():
    sql_connection = sqlite3.Connection
    sql_cursor = sqlite3.Cursor

    def __init__(self, path) -> None:
        try:
            self.sql_connection = sqlite3.connect(path)
            self.sql_cursor = self.sql_connection.cursor()
            print("Подключен к SQLite")
        except sqlite3.Error as error:
            print("Ошибка при работе с SQLite", error)

    def insert(self, table_name, coloms, values):
        sqlite_insert_query = f"""INSERT INTO {table_name}
                          ({coloms})
                          VALUES
                          ({values});"""
        self.sql_cursor.execute(sqlite_insert_query)
        self.sql_connection.commit()

    def updata(self, table_name, colom, value, condition):
        self.sql_cursor.execute(f'UPDATE {table_name} SET {colom} = {value} where {condition}')
        self.sql_connection.commit()

    def selectFrom(self, table_name, coloms):
        self.sql_cursor.execute(f'SELECT {coloms} FROM {table_name}')

        [print(row) for row in self.sql_cursor.fetchall()]

        return self.sql_cursor.fetchall()

    def selectFromWhere(self, table_name, coloms, condition):
        self.sql_cursor.execute(f'SELECT {coloms} FROM {table_name} WHERE {condition}')

        [print(row) for row in self.sql_cursor.fetchall()]
        
        return self.sql_cursor.fetchall()

    def insert_many(self, table_name : str, data : list) -> None:
        try:
            self.sql_cursor.executemany(f"INSERT INTO {table_name} VALUES { set_questions( len( data[0] ) ) }", data)
            self.sql_connection.commit()
        except sqlite3.Error as error:
            print(error)
        else:
            print(f"{table_name} was updated")

    def get_fieldNames(self) -> list:
        return list( map(lambda x: x[0], self.sql_cursor.description) )

    def update_database(self, data_folder : str) -> None:
        list_filenames = []

        sys.path.insert(0, os.path.abspath(f'./{data_folder}'))
        # print(sys.path)

        for (dirpath, dirnames, filenames) in os.walk(data_folder):
            list_filenames.extend(filenames)
            break

        # print(list_filenames)

        for file_name in list_filenames:
            table_name = file_name.split('.')[0]
            # print(table_name)
            # print( 'Path - ', sys.path[0] + '\\' + file_name )
            path = sys.path[0] + '\\' + file_name
            data = set_data_to_insert(path)

            if data == None : 
                print(f"{file_name} is empty")
                continue # Если в файле нет информации пропускаем данный файл

            self.insert_many(table_name, data)
        


def set_questions(len_cell : int) -> str:
    line = '('
    for i in range(len_cell):
        line += '?, '
    return line[:-2] + ')'

def set_data_to_insert(file_name : str) -> list:
    data = json_handler.read_json(file_name)

    if data == None: return None

    # print(data)

    cache = []
    for dicts in data:

        # print(dicts)

        list_cache = []
        for items in dicts.items():
            list_cache.append( items[1] )
        cache.append( tuple(list_cache) )
    return cache