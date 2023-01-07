from sqlite_handler import *

db_path = "SQLite\SQL_BD\gosha.sqlite"
json_folder_path = "SQLite\JSON_BD\Kolya"

obj = sqlite_handler(db_path)
obj.update_database(json_folder_path)
