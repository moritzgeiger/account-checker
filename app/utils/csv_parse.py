import pandas as pd
import csv
import xlsxwriter
from openpyxl import load_workbook
import openpyxl
import os
import streamlit as st
import csv
import io

PDF_DIRECTROY = '/Users/moritzgeiger/Desktop/acc'
EXCEL_DIRECTORY = '/Users/moritzgeiger/Desktop/excel/2021_Buchungen.xlsx'

class CSVHandler():
    def __init__(self):
        pass
    
    def parse(self, file):
        """"Parses csv bytes file.
        Returns: 
        pd.DataFrame()
        """
        # TODO: dynamic skiprows for various csv files
        byte_str = file.read()
        reader = csv.reader(io.StringIO(byte_str.decode("ISO-8859-1")))
        start = min([i for i, row in enumerate(reader) if 'Buchungstag' in row])
        date_columns = ['Buchungstag', 'Valuta']
        df = pd.read_csv(file, 
                        sep=';', 
                        skiprows=start, 
                        encoding="ISO-8859-1", 
                        decimal=',', 
                        thousands='.',
                        parse_dates=date_columns, 
                        dayfirst=True,
                        )
        df['Umsatz'] = df.Umsatz.astype(float)

        return df

    def save_row(self, row, sel_account, info, file_pdf, unique_n):
        """Saves user input and row contents to Excel file and pdf directory
        """
        
        if file_pdf:
            file_name = f'{unique_n}_{file_pdf.name}'
            with open(os.path.join(PDF_DIRECTROY, file_name),"wb") as f: 
                f.write(file_pdf.getbuffer())

        ### GET MAX ROW ### 
        wb = pd.read_excel(EXCEL_DIRECTORY, sheet_name='Journal')
        max_row = len(wb)

        df_dict = {}
        df_dict['Konto'] = [sel_account[:6]]
        df_dict['Kontoauswahl'] = [sel_account]
        df_dict['Datum'] = [row.Buchungstag]
        df_dict['Monat'] = [row.Buchungstag.month]
        if file_pdf:
            df_dict['Beleg'] = [file_pdf.name]
        else:
            df_dict['Beleg'] = ['Account']
        df_dict['Beschreibung'] = [info]
        df_dict['Ort'] = ['Invoice folder']
        df_dict['interne Ablage (NUR ZAHLEN)'] = [unique_n]
        df_dict['Betrag'] = [row.Umsatz]
        df_dict['unique_identifier'] = ''.join(row.astype(str))
        row_transformed = pd.DataFrame(df_dict)

        with pd.ExcelWriter(EXCEL_DIRECTORY, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            row_transformed.to_excel(writer, 'Journal', startrow=max_row+1, header=False, index=False)


    def validator(self, row):
        """Checks if row has been submitted to ExcelFile. 
        If row is new:
        _____
        Returns: 
        next row number for ExcelFile (int)"""

        wb = pd.read_excel(EXCEL_DIRECTORY, sheet_name='Journal')
        # validator column
        validator = list(wb.unique_identifier)
        uniqueness = ''.join(row.astype(str))
        if uniqueness in validator:
            return -999
        else:
            # return max internal reference number + 1
            max_n = wb['interne Ablage (NUR ZAHLEN)'].max() + 1
            return max_n

