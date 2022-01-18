import pandas as pd
import csv
    
class CSVHandler():
    def __init__(self):
        pass
    
    def parse(self, file):


        date_columns = ['Buchungstag', 'Valuta']
        df = pd.read_csv(file, 
                        sep=';', 
                        skiprows=15, 
                        encoding="ISO-8859-1", 
                        decimal=',', 
                        thousands='.',
                        parse_dates=date_columns, 
                        dayfirst=True,
                        )
        df['Umsatz'] = df.Umsatz.astype(float)

        return df

    def return_row(self, df):
        pass


