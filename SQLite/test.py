from sqlite_handler import *
# from pprint import pprint

# import sys, os
# sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем для получения содержимого папки Google_sheets_extension

# pprint(sys.path)

# import json_handler

# file_name = "SQLite\JSON_BD\Gosha\Answers.json"
# data = json_handler.read_json(file_name)
# pprint(data)

# cache = sqlite_handler.set_data_to_insert(file_name)

# pprint(cache)

# list_filenames = []
# data_folder = 'SQLite\JSON_BD\Gosha'
# for (dirpath, dirnames, filenames) in os.walk(data_folder):
#             list_filenames.extend(filenames)
#             break

# pprint(list_filenames)

db_path = "SQLite\SQL_BD\gosha.sqlite"
json_folder_path = "SQLite\JSON_BD\Kolya"

obj = sqlite_handler(db_path)
obj.update_database(json_folder_path)