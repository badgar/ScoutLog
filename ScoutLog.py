import pandas as pd
from pathlib import Path
import os
import shutil


def move_files(source, dest):
    files = source.glob('*table-data*')

    for f in files:
        shutil.move(f, dest)

def load_files():
    tab1 = pd.read_csv('table-data.csv')
    tab2 = pd.read_csv('table-data (1).csv')
    tab3 = pd.read_csv('table-data (2).csv')
    tab4 = pd.read_csv('table-data (3).csv')
    tab5 = pd.read_csv('table-data (4).csv')

    tab5.rename(columns={
        'Network': 'chain',
        'Address': 'address',
    }, inplace=True)

    return tab1, tab2, tab3, tab4, tab5


def concatenate_data(tab1, tab2, tab3, tab4, tab5):
    data_new = pd.concat([tab1, tab2, tab3, tab4]).reset_index()
    data_new.drop(data_new.columns[3:14], axis=1, inplace=True)
    data_new.drop('index', axis=1, inplace=True)
    tab5.drop(tab5.columns[2:13], axis=1, inplace=True)
    data_new = pd.concat([data_new, tab5]).reset_index()
    data_new.drop('index', axis=1, inplace=True)
    data_new['address'] = data_new['address'].str.strip('</a>').str.strip("<a href=").str[:-58].str.strip("'")
    return data_new


def check_and_export(data_new):
    if os.path.exists('data.csv') is True:
        data = pd.read_csv('data.csv', index_col=[0])
        to_check = pd.merge(data_new, data, on='address', how='left').reset_index()
        to_check = data_new.loc[~data_new['address'].isin(data['address'])]
        to_check.to_excel('to_check.xlsx', index=False)
        data = pd.concat([data, to_check]).reset_index()
        data.to_csv('data.csv')



def remove_files(dest):
    files_remove = dest.glob('*table-data*')
    for f in files_remove:
        os.remove(f)


source = Path('/Users/Kuba/Downloads')
dest = Path('/Users/Kuba/Desktop/ScoutLog')
move_files(source, dest)

tab1, tab2, tab3, tab4, tab5 = load_files()
data_new = concatenate_data(tab1, tab2, tab3, tab4, tab5)
check_and_export(data_new)
remove_files(dest)