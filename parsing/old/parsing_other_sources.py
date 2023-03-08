import requests
from bs4 import BeautifulSoup
import pandas as pd
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

def get_soup(strURL) -> BeautifulSoup:
    try:
        response = requests.get(strURL)
        print('Status code :', response.status_code)
    except:
        print("Connection error")
    soup = BeautifulSoup(response.text, "html.parser")
    return soup

def get_content(soup : BeautifulSoup, listNames : list, listColumns=['name','price','status']) -> pd.DataFrame:
    listTagsNames = listNames[0]
    listClassNames = listNames[1]
    if len(listClassNames) != len(listTagsNames): raise OwnError('Lens of input lists are not equal!')

    # df = pd.DataFrame(columns=listColumns[:len(listClassNames)])
    # print(type(soup))
    listContent = []
    for i in range(len(listClassNames)):
        content = soup.findAll(listTagsNames[i], class_=listClassNames[i])
        # print(type(content))
        # print(str(content))
        listSubjects = []
        for element in content:
            # print(element.text.strip().rstrip())
            strSubject = element.text.strip().rstrip()
            # print(type(strSubject))
            if listColumns[i] == 'price':
                strSubject = "".join([str(s) for s in strSubject.split() if s.isdigit()])

            if len(strSubject) > 3:
                listSubjects.append(strSubject)
        listContent.append(listSubjects)

    # df = pd.DataFrame(dict(zip(listColumns[:len(listClassNames)], listContent)))
    # print(df)
    # return df
    return pd.DataFrame(dict(zip(listColumns[:len(listClassNames)], listContent)))

def get_currentPart(soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
    soup = soup.findAll(strTagName, class_=strClassName)
    
    return BeautifulSoup(str(soup), "html.parser")

def make_jsonFile(df : pd.DataFrame, strFileName : str):
    with open(strFileName + '.json','w', encoding='utf-8') as file:
        file.write(df.to_json(force_ascii=False,indent=3))

def get_emptyDataframe(listColoms : list) -> pd.DataFrame:
    df = pd.DataFrame(dict(zip(listColoms, []*len(listColoms))))
    return df

def parsing(strFileName : str, strURL : str, listNames : list, extraStep, get_pageCount, listColumns):
    # print(get_pageCount(strURL))
    dfGeneral = get_emptyDataframe(listColumns) 
    for i in range(1, get_pageCount(strURL)+1):
        print(strURL + str(i))
        try: 
            soup = get_soup(strURL + str(i))
            soup = extraStep(soup)
            df = get_content(soup, listNames)
            # dfGeneral = pd.concat([dfGeneral, df])
            dfGeneral = dfGeneral.append(df)
        except Exception:
            break
        # print(df)
    dfGeneral.reset_index(inplace=True)
    dfGeneral = dfGeneral.drop(columns='index')
    # print(dfGeneral)
    make_jsonFile(dfGeneral, strFileName)

def get_pageCount_zero(strURL : str) -> int:
    return strURL

def get_pageCount_one(strURL : str) -> int:
    soup = get_soup(strURL)
    soup = get_currentPart(soup, 'span', 'nums') # Для https://wishmaster.me/catalog/smartfony/smartfony_apple/?sort=PRICE&order=desc&PAGEN_1=1'
    return  int(soup.text.strip().rstrip().split('\n')[-2])

def get_pageCount_two(strURL : str) -> int:
    soup = get_soup(strURL)
    soup = get_currentPart(soup, 'ul', 'pagination') # Для https://world-devices.ru/mobile_phones/apple_mobile/?limit=100&page=1
    hrefs = soup.find('a', href=True)
    # print(hrefs.text)

    return int(hrefs.text)

def get_pageCount_three(strURL : str) -> int:
    soup = get_soup(strURL)
    soup = get_currentPart(soup, 'a', 'pagination__item') # Для https://gsmbutik.ru/smartfony/apple/?page='
    intMax = 1
    for link in soup.find_all('a'):
        intMax = max(int(link.get('href').split('=')[1]), intMax)
    return intMax

def addition_zero(soup) -> BeautifulSoup:
    return soup

def addition_one(soup) -> BeautifulSoup:
    soup = get_currentPart(soup, 'div', 'col-sm-9') # Для https://world-devices.ru/mobile_phones/apple_mobile/?limit=100
    soup = get_currentPart(soup, 'div', 'row')      # Для https://world-devices.ru/mobile_phones/apple_mobile/?limit=100
    soup = get_currentPart(soup, 'div', 'row')      # Для https://world-devices.ru/mobile_phones/apple_mobile/?limit=100
    return soup

def main(listColumns=['name','price','status']):
    parsing('wishmaster',
            'https://wishmaster.me/catalog/smartfony/smartfony_apple/?sort=PRICE&order=desc&PAGEN_1=',
              [
                    ['h3','div','span'],
                    ['','product-card__content-price',['product-card__content-available','product-card__content-available no-img']]  # product-card__content-available no-img
              ],
              addition_zero,
              get_pageCount_one,
              listColumns
              )

    parsing('world-devices',
             'https://world-devices.ru/mobile_phones/apple_mobile/?limit=100&page=',
              [
                    ['a','span','div'],
                    ['','price-new', 'stock text-center'] 
              ],
              addition_one,
              get_pageCount_two,
              listColumns                          
              )

    parsing('gsmbutik',
             'https://gsmbutik.ru/smartfony/apple/?page=',
               [
                    ['div','div','div'],
                    ['catalog-list__name','catalog-list__cur-price','catalog-list__in-stock'] 
               ],
              addition_zero,
              get_pageCount_three,
              listColumns                          
              )
    
main()