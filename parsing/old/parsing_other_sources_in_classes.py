import requests
# from bs4 import BeautifulSoup
from bs4 import BeautifulSoup
import pandas as pd
import re
import support_function as sf

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
class Parsing():
    listNames   : list
    strFileName : str
    strURL      : str
    listColumns : list

    def __init__(self, strFileName : str, strURL : str, listNames : list, listColumns = ['name','price','status']) -> None:
        self.strFileName = strFileName
        self.strURL      = strURL
        self.listNames   = listNames
        self.listColumns = listColumns
        self.do_parsing()

    def get_pageCount(self) -> int:
        return 1

    def remove_duplicates(self, df : pd.DataFrame, strDubbedColum = 'name', strValuedolum = 'price') -> pd.DataFrame:
        dfDuplicat = df[df[strDubbedColum].duplicated() == True]
        dfCopy = df.drop_duplicates(subset = [strDubbedColum], keep = False)
        listNames = dfDuplicat[strDubbedColum].tolist()
        for strName in listNames:    
            dfVar = df.loc[df[strDubbedColum] == strName] # .isin(name)
            dfVar = dfVar[dfVar[strValuedolum] == dfVar[strValuedolum].min()]
            dfCopy =  pd.concat([dfCopy, dfVar])
        # dfCopy = dfCopy.drop_duplicates(subset = [strDubbedColum], keep = False)
        return dfCopy.drop_duplicates(subset = [strDubbedColum], keep = False)

    def addition_condition(self, soup : BeautifulSoup) -> BeautifulSoup:
        return soup 

    def get_emptyDataframe(self, listColoms : list) -> pd.DataFrame:
        df = pd.DataFrame(dict(zip(listColoms, []*len(listColoms))))
        return df

    def get_soup(self, strURL : str) -> BeautifulSoup:
        try:
            response = requests.get(strURL)
            print('Status code :', response.status_code)
        except:
            print("Connection error")
        soup = BeautifulSoup(response.text, "html.parser")
        return soup

    def make_jsonFile(self, df : pd.DataFrame, strFileName : str, strOrient = 'columns'):
        # strPath = '../small_test_project/parsing/data/'
        strPath = "parsing\data"
        with open(  strPath + strFileName + '.json','w', encoding='utf-8') as file:
            file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))

    def get_currentPart(self, soup : BeautifulSoup, strTagName : str, strClassName : str) -> BeautifulSoup: 
        soup = soup.findAll(strTagName, class_=strClassName)  
        return BeautifulSoup(str(soup), "html.parser")

    def get_deviceParameters(self, df : pd.DataFrame) -> pd.DataFrame:
        # listColors = ['White', 'Black', 'Green', 'Red', 'Purple', 'Yellow', 'Blue', 'Pink', 'Starlight', 'Gold', 'Silver',
        #             'Deep Purple', 'Space Black', 'Графитовый', 'Черный', 'Красный', 'Серый космос', 'Золотой', 'Серый'
        #             'Синий', 'Белый', 'Коралловый', 'Фиолетовый', 'Розовый', 'Зелёный', 'Желтый', 'Зеленый', 
        #             'Темная ночь', 'Альпийский зеленый', 'Небесно-голубой', 'Cеребристый', 'Космический черный',
        #             'Глубокий фиолетовый']


        listColors = ['white', 'black', 'green', 'red', 'purple', 'yellow', 'blue', 'pink', 'starlight', 'gold', 'silver', 'deep purple', 'space black', 'графитовый', 'черный',
                      'красный', 'серый космос', 'золотой', 'серый', 'синий', 'белый', 'коралловый', 'фиолетовый', 'розовый', 'зелёный', 'желтый', 'зеленый', 'темная ночь',
                      'альпийский зеленый', 'небесно-голубой', 'cеребристый', 'космический черный', 'глубокий фиолетовый','graphite', 'сияющая звезда']
        listMemory = ['16GB', '32GB', '64GB', '128GB', '256GB', '512GB', "1TB",'128 ГБ']
        listType = ['pro', 'pro max', 'mini', 'max', 'plus']
        listModel = ['8','9','10','11','12', '13' ,'14', 'xs', 'xr', 'se']
        
        dictReplacingColors = {'Белый': ['white', 'белый', 'starlight', 'сияющая звезда'],
                               'Графитовый': ['graphite', "графитовый"],
                               'Жёлтый': ['желтый', 'жёлтый', 'yellow'],
                               'Зелёный': ['green', 'зелёный', 'зеленый', 'альпийский зеленый'],
                               'Золотой': ['gold', 'золотой'],
                               'Коралловый': ['Coral','коралловый'],
                               'Красный': ['red','красный'],
                               'Темная ночь' : [ 'midnight', 'темная ночь'],
                               'Розовый': ['pink', 'розовый'],
                               'Космический черный': ['космический черный', 'space black', 'серый космос'],
                               'Серый': ['cеребристый','cерый космос', 'cерый'],
                               'Синий': ['blue', 'Небесно-Голубой'],
                               'Серебряный': ['silver','серебряный'],
                               'Фиолетовый': ['purple', 'фиолетовый', 'глубокий фиолетовый', 'deep purple'],
                               'Черный': ['тёмная ночь', 'black', 'черный', 'чёрный']
                               }
        # dictReplacingMemory =
        


        patternColors = '(?:{})'.format('|'.join(listColors))
        patternMemory = '(?:{})'.format('|'.join(listMemory))
        patternType   = '(?:{})'.format('|'.join(listType))
        patternModel  = '(?:{})'.format('|'.join(listModel))

        listValues = df['name'].values.tolist()

        listDeviceColors  = []
        listDeviceMemorys = []
        listDeviceTypes   = []
        listDeviceModels  = []

        for i in range( len(listValues)):
            # print(bool(re.search(pattern, listValues[i], flags=re.I)))
            try:
                strSameColor = (re.search(patternColors, listValues[i], flags=re.I)).group()
            except AttributeError:
                strSameColor = None
            try:
                strSameMemory = (re.search(patternMemory, listValues[i], flags=re.I)).group()
                strSameMemory = re.findall(r'\d+', strSameMemory)[0]
            except AttributeError:
                strSameMemory = None
            try:
                strSameType = (re.search(patternType, listValues[i], flags=re.I)).group()
                strSameType = strSameType.lower().title()
            except AttributeError:
                strSameType = None
                
            try:
                strSameModel = (re.search(patternModel, listValues[i], flags=re.I)).group()
                strSameModel = strSameModel.lower().title()
            except AttributeError:
                strSameModel = None
            


            for j in range( len(list(dictReplacingColors)) ):
                replPattern = '(?:{})'.format('|'.join(dictReplacingColors[list(dictReplacingColors)[j]]))
                try:
                    if bool(re.search(replPattern, strSameColor, flags=re.I)):
                        strSameColor = list(dictReplacingColors)[j]
                except Exception:
                    pass

            listDeviceColors.append( strSameColor )

            # re.findall(r'\d+', strSameMemory)

            listDeviceMemorys.append(strSameMemory)
            listDeviceTypes.append(  strSameType  )
            listDeviceModels.append( strSameModel )
            
            listValues[i] = 'IPhone ' + strSameModel 

            # print(listValues[i], ' - ', strSameColor, strSameMemory, strSameModel, strSameType)

        df = pd.DataFrame({'title': listValues ,'color': listDeviceColors, 'memory':listDeviceMemorys, 'type':listDeviceTypes, 'model':listDeviceModels})
        print(df)

        return df

    def get_content(self, soup : BeautifulSoup) -> pd.DataFrame:
        listTagsNames = self.listNames[0]
        listClassNames = self.listNames[1]
        if len(listClassNames) != len(listTagsNames): raise OwnError('Lens of input lists are not equal!')
        listContent = []
        for i in range(len(listClassNames)):
            content = soup.findAll(listTagsNames[i], class_=listClassNames[i])
            listSubjects = []
            for element in content:
                strSubject = element.text.strip().rstrip()
                # print(type(strSubject))
                # print(strSubject)
                if self.listColumns[i] == 'price':
                    strSubject = "".join([str(s) for s in strSubject.split() if s.isdigit()])    
                if len(strSubject) > 3:
                    listSubjects.append(strSubject)
            listContent.append(listSubjects)
        return pd.DataFrame(dict(zip(self.listColumns[:len(listClassNames)], listContent)))

    def do_parsing(self):
        dfGeneral = self.get_emptyDataframe(self.listColumns)
        listListHrefs = []

        for i in range(1, self.get_pageCount()+1):
            print(self.strURL + str(i))
            try: 
                soup = self.get_soup(self.strURL + str(i))

                soup = self.addition_condition(soup)

                df = self.get_content(soup)
                dfGeneral = pd.concat([dfGeneral, df])
                listListHrefs.append(self.get_hrefs(soup))
            except Exception:
                break

        dfHrefs = pd.DataFrame({'href': sum(listListHrefs, [])})
        dfParameters = self.get_deviceParameters(dfGeneral)
        dfGeneral.reset_index(inplace=True)
        dfGeneral = dfGeneral.drop(columns='index')
        dfGeneral['price'] = dfGeneral['price'].astype(int)

        dfGeneral = pd.concat([dfGeneral, dfHrefs, dfParameters], axis=1, join='inner')
        # dfGeneral = pd.concat([dfGeneral, dfColors], axis=1, join='inner')

        dfGeneral = self.remove_duplicates(dfGeneral)

        dfGeneral = dfGeneral.drop(['name','status'], axis=1)
        
        # dfGeneral.set_index(['title'], inplace = True)

        dfGeneral = dfGeneral.transpose()


        print(dfGeneral)
        
        self.make_jsonFile(dfGeneral, self.strFileName, )

class Wishmaster(Parsing):

    def __init__(self, strFileName : str, strURL : str, listNames : list, listColumns = ['name','price','status']) -> None:
        super().__init__(strFileName, strURL, listNames, listColumns)
    
    def get_pageCount(self):
        # soup = self.get_soup(self.strURL)
        soup = self.get_currentPart(self.get_soup(self.strURL), 'span', 'nums') # Для https://wishmaster.me/catalog/smartfony/smartfony_apple/?sort=PRICE&order=desc&PAGEN_1=1'
        return  int(soup.text.strip().rstrip().split('\n')[-2])

    def get_hrefs(self, soup : BeautifulSoup) -> list:
        soup = self.get_currentPart(soup, 'div', 'product-card__content')
        listHrefs = []
        for link in soup.find_all('a'):
            listHrefs.append(self.strURL.split('catalog')[0][:-1] + link.get('href'))
        return listHrefs

class WorldDevices(Parsing):

    def __init__(self, strFileName : str, strURL : str, listNames : list, listColumns = ['name','price','status']) -> None:
        super().__init__(strFileName, strURL, listNames, listColumns)
    
    def get_pageCount(self):
        # soup = get_soup(strURL)
        soup = self.get_currentPart(self.get_soup(self.strURL), 'ul', 'pagination') # Для https://world-devices.ru/mobile_phones/apple_mobile/?limit=100&page=1
        hrefs = soup.find('a', href=True)
        return int(hrefs.text)

    def addition_condition(self, soup : BeautifulSoup) -> BeautifulSoup:
        soup = self.get_currentPart(soup, 'div', 'col-sm-9') # Для https://world-devices.ru/mobile_phones/apple_mobile/?limit=100
        soup = self.get_currentPart(soup, 'div', 'row')      # Для https://world-devices.ru/mobile_phones/apple_mobile/?limit=100
        soup = self.get_currentPart(soup, 'div', 'row')      # Для https://world-devices.ru/mobile_phones/apple_mobile/?limit=100
        return soup 

    def get_hrefs(self, soup : BeautifulSoup) -> list:
        soup = self.get_currentPart(soup, 'div', 'name')
        listHrefs = []
        for link in soup.find_all('a'):
            listHrefs.append(link.get('href'))
        return listHrefs

class Gsmbutik(Parsing):
    def __init__(self, strFileName : str, strURL : str, listNames : list, listColumns = ['name','price','status']) -> None:
        super().__init__(strFileName, strURL, listNames, listColumns)
    
    def get_pageCount(self):
        # soup = get_soup(self, self.strURL)
        soup = self.get_currentPart(self.get_soup(self.strURL), 'a', 'pagination__item') # Для https://gsmbutik.ru/smartfony/apple/?page='
        intMax = 1
        for link in soup.find_all('a'):
            intMax = max(int(link.get('href').split('=')[1]), intMax)
        return intMax


    def get_hrefs(self, soup : BeautifulSoup) -> list:
        soup = self.get_currentPart(soup, 'div', 'catalog-list__name')
        listHrefs = []
        for link in soup.find_all('a'):
            listHrefs.append(link.get('href'))
        return listHrefs

Wishmaster('wishmaster.me', # One
        'https://wishmaster.me/catalog/smartfony/smartfony_apple/?sort=PRICE&order=desc&PAGEN_2=',
          [
                ['h3', 'div', 'span'],
                ['', 'product-card__content-price', ['product-card__content-available','product-card__content-available no-img']]  # product-card__content-available no-img
          ]
          )

# WorldDevices('world-devices.ru', # Two
#             'https://world-devices.ru/mobile_phones/apple_mobile/?limit=100&page=',
#             [
#                     ['a','span','div'],
#                     ['','price-new', 'stock text-center'] 
#             ]
#             )

Gsmbutik('gsmbutik.ru', # Three
         'https://gsmbutik.ru/smartfony/apple/?page=',
           [
                ['div','div','div'],
                ['catalog-list__name','catalog-list__cur-price','catalog-list__in-stock'] 
           ],
          )

df = sf.get_df()
df = df.drop_duplicates()
print(df)

strPath = 'parsing\data'
sf.make_jsonFile(df=df,strPath=strPath, strFileName="summary_file")