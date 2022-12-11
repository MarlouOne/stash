import sqlite3

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
    
