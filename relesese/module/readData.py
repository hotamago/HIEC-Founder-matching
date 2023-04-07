import pandas as pd
import os

class CsvData():
    def __init__(self, path = "list.csv"):
        self.path = path
        if not os.path.exists(self.path):
            ValueError('path %s not found' % self.path)
    def read(self, names, dtypes, valueNan = None):
        df = pd.read_csv('list.csv', header=0, names=list(names.values()), dtype=dtypes)
        df['id'] = range(0, len(df))

        df = df.fillna(value=valueNan)

        return df