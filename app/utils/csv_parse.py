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

    def save_row(self, row, file_path):
        with pd.ExcelWriter(file_path, engine='openpyxl', if_sheet_exists='overlay') as writer:
            row.to_excel(writer, 'Journal')


