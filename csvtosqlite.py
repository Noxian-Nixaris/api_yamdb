import os

import sqlite3
import pandas as pd

base = sqlite3.connect('api_yamdb/db.sqlite3')


def load_data_from_csv():
    files = os.listdir('api_yamdb/static/data/')

    for file in files:
        file_name = file.split('.csv')[0]
        csv_file = pd.read_csv(f'api_yamdb/static/data/{file_name}.csv')
        try:
            if file_name == 'users':
                csv_file.to_sql(
                    'authuser_user',
                    base, if_exists='replace',
                    index=False
                )
            else:
                csv_file.to_sql(
                    f'reviews_{file_name}',
                    base, if_exists='replace',
                    index=False
                )
        except Exception:
            continue


if __name__ == '__main__':

    load_data_from_csv()
