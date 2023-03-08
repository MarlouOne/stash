'''
Европа :
https://www.banggood.com/ru/buy/germany-drone/8768-0-0-1-1-60-0-price-0-0_p-1.html
'''


import requests
# from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
from pprint import pprint
import re
# import support_function as sf

class OwnError(Exception):
    def __init__(self, *args: object) -> None:
        if args:
            self.message = args[0]
        else:
            self.message = None
    
    def __str__(self) -> str:
        if self.message:
            return 'OwnError, {0} '.format(self.message)
        else:
            return 'OwnError has been raised!'

def get_soup(strURL : str) -> BeautifulSoup:
    try:
        response = requests.get(strURL)
        print('Status code :', response.status_code)
    except:
        print("Connection error")
    soup = BeautifulSoup(response.text, "html.parser") # "html.parser"
    return soup        

def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup_copy = soup
    soup_copy = soup.findAll(strTagName, class_=strClassName)  
    return BeautifulSoup(str(soup_copy), "html.parser")

def get_hrefs( soup : BeautifulSoup) -> list:
    soup = get_currentPart(soup, 'span', 'img notranslate')
    listHrefs = []
    for link in soup.find_all('a'):
        listHrefs.append(link.get('href'))
    return listHrefs

def get_pageCount(soup : BeautifulSoup) -> int:
    soup = get_currentPart(soup, 'div', 'num')
    return  int(soup.text.strip().rstrip().split('\n')[-2])
    
def get_emptyDataframe( listColoms : list) -> pd.DataFrame:
    df = pd.DataFrame(dict(zip(listColoms, []*len(listColoms))))
    return df

def get_spec_alt(soup : BeautifulSoup) -> dict:
    spec = soup.find('div', attrs={"style": "font-size:14px;"}) # style="font-size:14px;" .get_text('|', strip=True)
    specifications = {}
    
    for case in spec:
        case = case.get_text('|', strip=True)
        case = case.split("|")[2:]
        for item in case:
            content = item.split(':')
            if len( content ) == 2 and content[1] != '':
                specifications[content[0]] = content[1]
    return specifications

def get_spec(soup : BeautifulSoup) -> dict:
    spec = soup.find('div', class_='cont' ,attrs={"data-spm": "0000000UX"}).get_text('|', strip=True)
    spec = spec.split("|")[2:]
    specifications = {}
    
    for item in spec:
        content = item.split(':')
        if len( content ) == 2 and content[1] != '':
            specifications[content[0]] = content[1]
    return specifications

def get_content(soup : BeautifulSoup, listColumns : list) -> pd.DataFrame:
    try:
        tag = soup.find('span', attrs={"data-spm": "00000000a-3"}).get_text('|', strip=True)
    except Exception:
        tag = "None"
    
    try:
        brand = soup.find('a', attrs={"data-spm": "0000000Au"}).get_text('|', strip=True)
    except Exception:
        brand = "None"
        
    name =  soup.find('span', attrs={"data-spm": "0000000Ap"}).get_text('|', strip=True)
    # price = soup.find('span', class_='main-price', attrs={"data-spm": "0000000Bf"}).get_text('|', strip=True)
    price = 'None'
    
    
    try:
        specifications = get_spec(soup)
    except Exception:
        try:
            specifications = get_spec_alt(soup)
        except:
            specifications = 'None'
    
    # result = {listColumns[0]: tag, listColumns[1]: brand, listColumns[2]: name, listColumns[3]: price, listColumns[4]: specifications} 
    
    return pd.DataFrame([tag, brand, name, price, specifications], index = listColumns)

    # df = pd.DataFrame(list_values,index = ['i', 'ii', 'iii', 'iv', 'v'], columns = ['Subjects'])
    
def make_jsonFile(strPath, df : pd.DataFrame, strFileName : str, strOrient = 'records'):
    # strPath = '../small_test_project/parsing/data/'
    # strPath = "parsing\data"
    with open(  strPath + '\\' + strFileName + '.json','w', encoding='utf-8') as file:
        file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))
    
# def to_json(file_path : str, df : pd.DataFrame) -> None: # Запись в JSON файл без сохранение старого содержимого
#     with open(file_path, 'w') as file:
#         result = df.to_json (orient='records')
#         parsed = json.loads(result)
#         file.write(result)
    
def main() -> None:
    strURL = 'https://www.banggood.com/ru/buy/germany-drone/8768-0-0-1-1-60-0-price-0-0_p-1.html' # Первая страница
    # strURL = 'https://www.banggood.com/ru/buy/germany-drone/8768-0-0-1-1-60-0-price-0-0_p-2.html' # Вторая страница
    
    listColumns = ['tag', 'brand', 'name','price','specifications']
    file_path = "parsing\data"
    
    soup = get_soup(strURL) # Получаем содержимое страници 
    last_page = get_pageCount( soup )  # Получаем количество подстраниц
    dfGeneral = get_emptyDataframe(listColumns) # Создаём пустой pd.dataframe с столбцами из listColumns
    
    listTagsNames = [
                        ['span', 'span', 'div'],
                        ["product-title-text", "main-price", "tab-cnt"]
                    ]
    # last_page = 1
    
    for index in range(1, last_page ): # Проходим по всем страницам с деталями
        strURL = f'https://www.banggood.com/ru/buy/germany-drone/8768-0-0-1-1-60-0-price-0-0_p-{index}.html' # Страница с определённым индексом
        soup = get_soup(strURL) # Получаем содержимое страници 
        hrefs = get_hrefs(soup) # Получаем ссылки на продукты на данной странице
        for href in hrefs:    
            print(href)
            soup = get_soup(href) # Получаем содержимое страници с определённой позицией
            df = get_content(soup, listColumns) # Получаем набор записей о позиции
            df = df.transpose()
            # print(df)
            dfGeneral = pd.concat([dfGeneral, df])
            
    print(dfGeneral)
    make_jsonFile(file_path, dfGeneral, 'data')
    
    # print( soup.div )
    # print( soup.find_all('div', class_= 'num') )

    
main()