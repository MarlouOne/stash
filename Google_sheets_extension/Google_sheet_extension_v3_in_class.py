# This is basic Google Sheet extension that can work with them.
# Habr link - https://habr.com/ru/post/483302/
# YouTobe video link - https://www.youtube.com/watch?v=hMl-0yiBMNs&list=PLWVnIRD69wY75tQAmyMFP-WBKXqJx8Wpq&index=1


# Sirvice account email - acc-634@pythonextension.iam.gserviceaccount.com
# Sirvice account JSON key contain in pythonextension-202bab519501.json file.

# pip install --upgrade google-api-python-client
# pip install oauth2client
# quickestart.py contain content from https://raw.githubusercontent.com/gsuitedevs/python-samples/master/sheets/quickstart/quickstart.py


myGmail = 'majorstol@gmail.com'

# Подключаем библиотеки
import os
import httplib2 
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials	

from pprint import pprint

import inspect

def showVarType(var) -> None: # Узнаём тип данных произвольной переменной
    caller_locals = inspect.currentframe().f_back.f_locals
    varName = [name for name, value in caller_locals.items() if var is value] # Получаем имя переменной 
    print(var, f'\n{varName} type is {type(var)}') # Узнаём тип данных переменной 


class extension(): # Класс отвечающий за работу с google sheet
    CREDENTIALS_FILE : str  # Путь к фалу с клучом от сервесного аккаунта
    service          : build # Служба для работы с таблицей
    sheet            : build # Все листы в таблице
    sheet_id         : str  # ID нужной нам Google sheet
    
    def __init__(self, CREDENTIALS_FILE, sheet_id) -> None:
        try:
            self.CREDENTIALS_FILE = CREDENTIALS_FILE  # Имя файла с закрытым ключом, вы должны подставить свое
            self.service = self.get_sheet_service() # Создаём службу для работы с таблицей
            self.sheet   = self.service.spreadsheets() 
            self.sheet_id = sheet_id # ID нужной нам Google sheet
        except Exception:
            print('Can not connect extention !')
        else:
            print('Extention connected !')

    def get_sheet_service(self): # Получаем доступ к нужной таблице с заранее подключенным потом
        json = os.path.dirname(__file__) + '\\' + self.CREDENTIALS_FILE
        print(json)
        scopes = ['https://www.googleapis.com/auth/spreadsheets']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(json,scopes).authorize(httplib2.Http())
        return build('sheets','v4', http=credentials)

    def get_sheetsId(self) -> dict: # Получаем словарь имен листов и их Id 
        spreadsheet = self.service.spreadsheets().get(spreadsheetId = self.sheet_id).execute()
        dictSheets = {}
        for sheet in spreadsheet.get('sheets'):
            dictSheets [sheet['properties']['title']] = sheet['properties']['sheetId']
        return dictSheets

    def show_sheetInfo(self, ranges = list, includeGridData = True): # Функция вывода информации об интервале ячеек "range=['Лист номер один!C2:C2']"
        results = self.service.spreadsheets().get(spreadsheetId = self.spreadsheetId, 
                                            ranges = ranges, includeGridData = includeGridData).execute()
        print('Основные данные')
        print(results['properties'])
        print('\nЗначения и раскраска')
        print(results['sheets'][0]['data'][0]['rowData'] )
        print('\nВысота ячейки')
        print(results['sheets'][0]['data'][0]['rowMetadata'])
        print('\nШирина ячейки')
        print(results['sheets'][0]['data'][0]['columnMetadata'])


    def read_sheet(self, range : str) -> dict: # Чтение из таблицы
        return self.sheet.values().get(spreadsheetId = self.sheet_id, range = range).execute() 

    def add_newSheet(self, sheetTitle = "New sheet", rowCount = 20, columnCount = 20) -> None: # Созадание новой таблицы
        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId = self.sheet_id,
                body = 
                {"requests": [{"addSheet": {
                                            "properties": {
                                            "title": sheetTitle,
                                            "gridProperties": {
                                                            "rowCount": rowCount,
                                                                "columnCount": columnCount
                                                            }
                                                        }
                                            }
                                }
                            ]
                }
            ).execute()
        except Exception:
            print(f'Sheet with name {sheetTitle} already exists, "add_newSheet" query - aborted  !')

    def add_tableTitle(self, range : str, values : list): # Добавляем заголовок таблицы "values = ['Заголовок таблицы']"
        try:
            self.service.spreadsheets().values().batchUpdate(spreadsheetId = self.sheet_id, body = {
                "valueInputOption": "USER_ENTERED",
            # Данные воспринимаются, как вводимые пользователем (считается значение формул)
                "data": [
                    {"range": range,
                    "majorDimension": "ROWS", # Сначала заполнять строки, затем столбцы
                    "values": [ values ]}
                ]
            }).execute()
        except Exception:
            print('Incorrect input data, "add_tableTitle" query - aborted !')
        print('"add_tableTitle" query - done !')

    def insert_data(self, range : str, values : list, majorDimension = "ROWS") -> None: # Вставка данных в таблицу
        try:
            self.service.spreadsheets().values().batchUpdate(spreadsheetId = self.sheet_id, body = {
                "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
                "data": [
                            {
                            "range": range,
                            "majorDimension": majorDimension,     # Сначала заполнять строки, затем столбцы
                            "values": values
                            }
                        ]
            }).execute()
        except Exception:
            print('Incorrect input data, "insert_data" query - aborted !')
        print('"insert_data" query - done !')

    def set_COLUMNS_width(self, sheetId : int, startIndex = 0, endIndex = 1, pixelSize = 20, fields = "pixelSize"): # Задать ширину столбца 
        try:
            self.service.spreadsheets().batchUpdate(spreadsheetId = self.sheet_id, body = {
            "requests":  
                    {
                    "updateDimensionProperties": 
                    {
                        "range": {
                        "sheetId": sheetId, # ID Листа 
                        "dimension": "COLUMNS",  # Задаем ширину колонки
                        "startIndex": startIndex, # Нумерация начинается с нуля
                        "endIndex": endIndex # Со столбца номер startIndex по endIndex - 1 (endIndex не входит!)
                                },
                        "properties": {
                        "pixelSize": pixelSize # Ширина в пикселях
                                    },
                        "fields": fields # Указываем, что нужно использовать параметр pixelSize  
                    }
                    },
                }).execute()
        except Exception:
            print('Incorrect input data, "set_COLUMNS_width" query - aborted !')
        print('"set_COLUMNS_width" query - done !')

    def set_frame(self, sheetId : int, startRowIndex : int, endRowIndex : int, startColumnIndex : int, endColumnIndex : int, borderWidth = 1, style = 'SOLID'): # Рисуем рамку
        try:
            self.service.spreadsheets().batchUpdate(
                spreadsheetId = self.sheet_id,
                body = {
                    "requests": [
                        {'updateBorders': {'range': {'sheetId': sheetId,
                                        'startRowIndex': startRowIndex,
                                        'endRowIndex': endRowIndex,
                                        'startColumnIndex': startColumnIndex,
                                        'endColumnIndex': endColumnIndex},
                            'bottom': {  
                            # Задаем стиль для верхней границы
                                        'style': style, # Сплошная линия
                                        'width': borderWidth,       # Шириной 1 пиксель
                                        'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}, # Черный цвет
                            'top': { 
                            # Задаем стиль для нижней границы
                                        'style': style,
                                        'width': borderWidth,
                                        'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                            'left': { # Задаем стиль для левой границы
                                        'style': style,
                                        'width': borderWidth,
                                        'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                            'right': { 
                            # Задаем стиль для правой границы
                                        'style': style,
                                        'width': borderWidth,
                                        'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                            'innerHorizontal': { 
                            # Задаем стиль для внутренних горизонтальных линий
                                        'style': style,
                                        'width': borderWidth,
                                        'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                            'innerVertical': { 
                            # Задаем стиль для внутренних вертикальных линий
                                        'style': style,
                                        'width': borderWidth,
                                        'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}
                                        
                                        }}
                    ]
                }).execute()
        except Exception:
            print('Incorrect input data, "set_frame" query - aborted !')
        print('"set_frame" query - done !') 

    def merge_cells(self, sheetId : int, startRowIndex : int, endRowIndex : int, startColumnIndex : int, endColumnIndex : int, mergeType = 'MERGE_ALL'): # Объединяем ячейки 
        self.service.spreadsheets().batchUpdate(
            spreadsheetId = self.sheet_id,
            body = {
                "requests": [
                    {'mergeCells': {'range': {'sheetId': sheetId,
                                'startRowIndex': startRowIndex,
                                'endRowIndex': endRowIndex,
                                'startColumnIndex': startColumnIndex,
                                'endColumnIndex': endColumnIndex},
                        'mergeType': mergeType}}
                ]
            }).execute()

        # Установка формата ячеек
    def set_format(self, sheetId : int, startRowIndex : int, endRowIndex : int, startColumnIndex : int, endColumnIndex : int, horizontalAlignment = 'CENTER', listCalor = [0.8, 0.8, 0.8, 1], bold = True, fontSize = 14):
        self.service.spreadsheets().batchUpdate(
            spreadsheetId = self.sheet_id,
            body = 
        {
        "requests": 
        [
            {
            "repeatCell": 
            {
                "cell": 
                {
                "userEnteredFormat": 
                {
                    "horizontalAlignment": horizontalAlignment,
                    "backgroundColor": {
                        "red":   listCalor[0],
                        "green": listCalor[1],
                        "blue":  listCalor[2],
                        "alpha": listCalor[3]
                    },
                    "textFormat":
                    {
                    "bold": bold,
                    "fontSize": fontSize
                    }
                }
                },
                "range": 
                {
                "sheetId": sheetId,
                "startRowIndex"     : startRowIndex,
                "endRowIndex"       : endRowIndex,
                "startColumnIndex"  : startColumnIndex,
                "endColumnIndex"    : endColumnIndex
                },
                "fields": "userEnteredFormat"
            }
            }
        ]
        }).execute()





def main():
    CREDENTIALS_FILE = 'pythonextension-202bab519501.json'  # Имя файла с закрытым ключом, вы должны подставить свое
    sheet_id = '1s7CcKw-uDbmjeSDgiB_jQQ2CwYq3t14k0Y_3kxO2KqA' # ID нужной нам Google sheet    # https://docs.google.com/spreadsheets/d/1s7CcKw-uDbmjeSDgiB_jQQ2CwYq3t14k0Y_3kxO2KqA/edit#gid=937792580

    obj = extension(CREDENTIALS_FILE,sheet_id)      # Ok
    print(obj.get_sheetsId())                       # Ok
    obj.add_newSheet(sheetTitle='Лист4')            # Ok
    pprint(obj.read_sheet('Лист4'))                 # Ok
    sheetsID = obj.get_sheetsId()

    obj.add_tableTitle('Лист4!D1',['ХУЙ','ЗАЛУПА']) # Ok
    obj.insert_data('Лист4!B6',[[4,5,6],[9,8,7]])   # Ok
    obj.set_COLUMNS_width(sheetsID['Лист4'], 2, 4, 100)  # Ok
    obj.set_frame(sheetsID['Лист4'], 0, 3, 0, 3)    # Ok
    obj.merge_cells(sheetsID['Лист4'], 5, 5,  5, 6)  # Ok
    obj.set_format(sheetsID['Лист4'], )

if __name__ == '__main__': # Если файл tg_bot.py вызаван, то будет запущен main(strBotToken); Если он будет импортироват то ничего не произайдёт
    main()

print('Google_sheet_extension_v3_in_class is here !')