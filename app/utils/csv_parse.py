import pandas as pd
import csv
import xlsxwriter
from openpyxl import load_workbook
import openpyxl
import os
import streamlit as st
import csv
import io

class CSVHandler():
    def __init__(self):
        pass

    def return_start(self, file):
        byte_str = file.getvalue().splitlines()
        return min([i for i, row in enumerate(byte_str) if 'Buchungstag' in str(row)[:20]])

    def parse(self, file):
        """"Parses csv bytes file.
        Returns:
        pd.DataFrame()
        """
        date_columns = ['Buchungstag', 'Valuta']
        start = self.return_start(file)
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

