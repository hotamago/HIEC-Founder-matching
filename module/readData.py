import pandas as pd
import os

class CsvData():
    def __init__(self, path = "list.csv"):
        self.path = path
        if not os.path.exists(self.path):
            ValueError('path %s not found' % self.path)
    def read(self, names, valueNan = ""):
        # check if list.csv is exist
        if not os.path.exists('list.csv'):
            # create list.csv by list_example.csv
            with open('list_example.csv', 'r') as f:
                with open('list.csv', 'w') as f2:
                    f2.write(f.read())     

        # read list.csv
        df = pd.read_csv('list.csv', header=0, names=list(names), dtype=str)
        df['id'] = range(0, len(df))

        df = df.fillna(value=valueNan)

        return df