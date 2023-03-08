import os, fnmatch
import pandas as pd

#strVar = df.to_string() # dataframe в str

def get_df(pattern = "*.json" , strTopFolder = '../small_test_project/parsing/data/'):
    return get_dfFromJSONFile(get_listCurrentContent(pattern,strTopFolder))


def get_dfFromJSONFile(listFilesPath : list) -> pd.DataFrame:
    df = pd.DataFrame()
    for strFilePath in listFilesPath:
        df = pd.concat([df, pd.read_json(strFilePath).transpose()])
    return df

def get_listCurrentContent(strPattern = "*.json" , strTopFolder = '../small_test_project/tg_bot/data/'):
    listResult = []
    for dirpath, dirnames, filenames in os.walk(strTopFolder):
        for filename in filenames:
            if fnmatch.fnmatch(filename, strPattern):
                listResult.append(os.path.join(dirpath, filename))
    # print(listResult)
    return listResult

def make_jsonFile( df : pd.DataFrame,strPath : str, strFileName : str, strOrient = 'columns'):
    # strPath = '../small_test_project/parsing/data/'
    # strPath = '../small_test_project/parsing/data/'
    with open(  strPath + strFileName + '.json','w', encoding='utf-8') as file:
        file.write(df.to_json(force_ascii=False, indent=3, orient=strOrient))

def do_writeInFile(strFilePath : str, strContent : str, mode = 'w') -> None:
    with open(strFilePath, mode, encoding='utf-8') as file:
        file.write(strContent)

def get_listUniqueValues(df : pd.DataFrame, strKey : str) -> list:
    return df[strKey].unique().tolist()