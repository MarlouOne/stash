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
import httplib2 
import apiclient.discovery
from oauth2client.service_account import ServiceAccountCredentials	


CREDENTIALS_FILE = 'Google_sheets_extension\pythonextension-202bab519501.json'  # Имя файла с закрытым ключом, вы должны подставить свое
# Читаем ключи из файла

def get_services(credentialsFilePath : str):
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentialsFilePath, ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive'])
    httpAuth = credentials.authorize(httplib2.Http()) # Авторизуемся в системе
    sheetService = apiclient.discovery.build('sheets', 'v4', http = httpAuth) # Выбираем работу с таблицами и 4 версию API 
    driveService = apiclient.discovery.build('drive', 'v3', http = httpAuth) # Выбираем работу с Google Drive и 3 версию API
    return sheetService, driveService

def get_spreadsheetId(sheetService, sheetTile = 'Первый тестовый документ', firstPageTitle = 'Лист номер один'): # Создаём таблицу
    spreadsheet = sheetService.spreadsheets().create(body = {
    'properties': {'title': sheetTile, 'locale': 'ru_RU'},
    'sheets': [{'properties': {'sheetType': 'GRID',
                               'sheetId': 0,
                               'title': firstPageTitle,
                               'gridProperties': {'rowCount': 100, 'columnCount': 15}}}]
    }).execute()
    spreadsheetId = spreadsheet['spreadsheetId'] # сохраняем идентификатор файла
    print('https://docs.google.com/spreadsheets/d/' + spreadsheetId)
    return spreadsheetId

def get_access_by_gmail(driveService, spreadsheetId, gmail): # Открываем доступ на редактирование к таблице
    driveService.permissions().create(
    fileId = spreadsheetId,
    body = {'type': 'user', 'role': 'writer', 'emailAddress': gmail},  # Открываем доступ на редактирование
    fields = 'id'
    ).execute()

# Добавление листа
def add_newSheet(service, spreadsheetId, sheetTitle = "Еще один лист", rowCount = 20, columnCount = 20):
    service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheetId,
        body = 
    {
    "requests": [
        {
        "addSheet": {
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
    }).execute()

# Получаем список листов, их Id и название
def get_sheetId(service, spreadsheetId):
    spreadsheet = service.spreadsheets().get(spreadsheetId = spreadsheetId).execute()
    sheetList = spreadsheet.get('sheets')
    for sheet in sheetList:
        print(sheet['properties']['sheetId'], sheet['properties']['title'])

    sheetId = sheetList[0]['properties']['sheetId']
    print('Мы будем использовать лист с Id = ', sheetId)
    return sheetId

def insert_data(service, spreadsheetId, range = "Лист номер один!B2:D5", majorDimension = "ROWS", 
                values = [
                            ["Ячейка B2", "Ячейка C2", "Ячейка D2"], # Заполняем первую строку
                            ['25', "=6*6", "=sin(3,14/2)"]  # Заполняем вторую строку
                         ]):

    service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED", # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": range,
            "majorDimension": majorDimension,     # Сначала заполнять строки, затем столбцы
            "values": values}
        ]
    }).execute()

def set_COLUMNS_width(service, spreadsheetId, sheetId, startIndex = 0, endIndex = 1, pixelSize = 20, fields = "pixelSize"): # Задать ширину столбца 
   service.spreadsheets().batchUpdate(spreadsheetId = spreadsheetId, body = {
  "requests":  
        {
        "updateDimensionProperties": 
        {
            "range": {
            "sheetId": sheetId,
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

def set_frame(service, spreadsheetId, sheetId, startRowIndex = 1, endRowIndex = 3, startColumnIndex = 1, endColumnIndex = 4, borderWidth = 1):
    # Рисуем рамку
    service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheetId,
        body = {
            "requests": [
                {'updateBorders': {'range': {'sheetId': sheetId,
                                'startRowIndex': startRowIndex,
                                'endRowIndex': endRowIndex,
                                'startColumnIndex': startColumnIndex,
                                'endColumnIndex': endColumnIndex},
                    'bottom': {  
                    # Задаем стиль для верхней границы
                                'style': 'SOLID', # Сплошная линия
                                'width': borderWidth,       # Шириной 1 пиксель
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}, # Черный цвет
                    'top': { 
                    # Задаем стиль для нижней границы
                                'style': 'SOLID',
                                'width': borderWidth,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                    'left': { # Задаем стиль для левой границы
                                'style': 'SOLID',
                                'width': borderWidth,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                    'right': { 
                    # Задаем стиль для правой границы
                                'style': 'SOLID',
                                'width': borderWidth,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                    'innerHorizontal': { 
                    # Задаем стиль для внутренних горизонтальных линий
                                'style': 'SOLID',
                                'width': borderWidth,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}},
                    'innerVertical': { 
                    # Задаем стиль для внутренних вертикальных линий
                                'style': 'SOLID',
                                'width': borderWidth,
                                'color': {'red': 0, 'green': 0, 'blue': 0, 'alpha': 1}}
                                
                                }}
            ]
        }).execute()

def merge_cells(service , spreadsheetId, sheetId, startRowIndex = 0, endRowIndex = 1, startColumnIndex = 1, endColumnIndex = 4): # Объединяем ячейки 
    service.spreadsheets().batchUpdate(
        spreadsheetId = spreadsheetId,
        body = {
            "requests": [
                {'mergeCells': {'range': {'sheetId': sheetId,
                            'startRowIndex': startRowIndex,
                            'endRowIndex': endRowIndex,
                            'startColumnIndex': startColumnIndex,
                            'endColumnIndex': endColumnIndex},
                    'mergeType': 'MERGE_ALL'}}
            ]
        }).execute()

def add_tableTitle(service, spreadsheetId, range = "Лист номер один!B1", values = ["Заголовок таблицы"]): # Добавляем заголовок таблицы
    service.spreadsheets().values().batchUpdate(spreadsheetId = spreadsheetId, body = {
        "valueInputOption": "USER_ENTERED",
    # Данные воспринимаются, как вводимые пользователем (считается значение формул)
        "data": [
            {"range": range,
            "majorDimension": "ROWS", # Сначала заполнять строки, затем столбцы
            "values": [ values ]}
        ]
    }).execute()

def show_sheetInfo(service, spreadsheetId, ranges = ["Лист номер один!C2:C2"], includeGridData = True):
    results = service.spreadsheets().get(spreadsheetId = spreadsheetId, 
                                        ranges = ranges, includeGridData = True).execute()
    print('Основные данные')
    print(results['properties'])
    print('\nЗначения и раскраска')
    print(results['sheets'][0]['data'][0]['rowData'] )
    print('\nВысота ячейки')
    print(results['sheets'][0]['data'][0]['rowMetadata'])
    print('\nШирина ячейки')
    print(results['sheets'][0]['data'][0]['columnMetadata'])

service, driveService = get_services(CREDENTIALS_FILE)

spreadsheetId = get_spreadsheetId(service)
get_access_by_gmail(driveService, spreadsheetId, myGmail)
add_newSheet(service, spreadsheetId)
sheetId = get_sheetId(service, spreadsheetId)
insert_data(service, spreadsheetId)
set_COLUMNS_width(service, spreadsheetId, sheetId)
set_frame(service, spreadsheetId, sheetId)
merge_cells(service, spreadsheetId, sheetId)
add_tableTitle(service, spreadsheetId)
show_sheetInfo(service, spreadsheetId)


# # Установка формата ячеек
# results = service.spreadsheets().batchUpdate(
#     spreadsheetId = spreadsheetId,
#     body = 
# {
#   "requests": 
#   [
#     {
#       "repeatCell": 
#       {
#         "cell": 
#         {
#           "userEnteredFormat": 
#           {
#             "horizontalAlignment": 'CENTER',
#             "backgroundColor": {
#                 "red": 0.8,
#                 "green": 0.8,
#                 "blue": 0.8,
#                 "alpha": 1
#             },
#             "textFormat":
#              {
#                "bold": True,
#                "fontSize": 14
#              }
#           }
#         },
#         "range": 
#         {
#           "sheetId": sheetId,
#           "startRowIndex": 1,
#           "endRowIndex": 2,
#           "startColumnIndex": 1,
#           "endColumnIndex": 4
#         },
#         "fields": "userEnteredFormat"
#       }
#     }
#   ]
# }).execute()