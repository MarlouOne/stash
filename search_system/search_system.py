# from googlesearch import search
# query = "СВО"
# for i in search(query, tld="ru", num=10, stop=10, pause=2): print(i)

import sys, os
sys.path.insert(0, os.path.abspath('./')) # Добавляем папку выше уровнем для получения содержимого папки Google_sheets_extension

import json_handler
from pprint import pprint
import requests

class search_system():
    API_KEY : str
    SEARCH_ENGINE_ID : str

    def __init__(self, api_key : str, search_engine_id : str) -> None:
        self.API_KEY = api_key
        self.SEARCH_ENGINE_ID = search_engine_id    
        

    def search(self, query : str, page = 1 ) -> list:
        start = (page - 1) * 10 + 1        
        url = f"https://www.googleapis.com/customsearch/v1?key={self.API_KEY}&cx={self.SEARCH_ENGINE_ID}&q={query}&start={start}"    
        data = requests.get(url).json() # make the API request
        return data.get("items") # get the result items
    
    def show_search_resualt(self, search_resualts : list) -> None:
        for item in search_resualts: 
            print("="*10, f"Результат №{search_resualts.index(item)}", "="*10)
            print("Заголовок:", item['title'])
            print("Описание:", item['description'])
            print("Большое описание:", item['long_description'])
            print("URL:", item['URL'], "\n")

    def wrap_resualt(self, search_resualts : list) -> list:
        wrapped_list = []

        for i, search_resualts in enumerate(search_resualts, start=1): # iterate over 10 results found
            try:
                long_description = search_resualts["pagemap"]["metatags"][0]["og:description"]
            except KeyError:
                long_description = "N/A"

            wrapped_list.append( {"title": search_resualts.get("title"),"description": search_resualts.get("snippet"),"long_description": long_description, "URL": search_resualts.get("link")} )

        return wrapped_list

    def save_json(self, file_path : str , search_resualts : list) -> None:
        json_handler.add_json(file_path, search_resualts)

def test():
    system = search_system('AIzaSyBtVaNmzMLk8DbjdNh0Mq_OqyNN5QvcnY0', "d75c9236c9f8e4053")
    resualts = system.search('Путин')   
    resualts = system.wrap_resualt(resualts) 
    system.show_search_resualt(resualts)

    file_path = 'search_resualt.json'
    system.save_json(file_path, resualts)

def main(api_key : str, search_engine_id : str) -> None:
    system = search_system(api_key, search_engine_id)
    
    while True:
        search = input('Введите поисковый запрос :')
        resualts = system.search(search)
        resualts = system.wrap_resualt(resualts) 
        system.show_search_resualt(resualts)

        file_path = 'search_resualt.json'
        system.save_json(file_path, resualts)
        if input("Продолжить? (Да/Нет)") == "Нет": break

    input("Press Enter to continue...")

if __name__ == '__main__':
    main('AIzaSyBtVaNmzMLk8DbjdNh0Mq_OqyNN5QvcnY0', "d75c9236c9f8e4053")
    # test()




