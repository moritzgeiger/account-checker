
import pandas as pd
import csv
import xlsxwriter
from openpyxl import load_workbook
import openpyxl
import os
import streamlit as st
import csv
import io
import json

PDF_DIRECTROY = 'temp'
SCHEMA_TARGET = "utils/schema_target.json"

class ExcelWriter():

  def save_row(self, row, sel_account, info, file_pdf, unique_n):
      """Saves user input and row contents to Excel file and pdf directory
      Returns:
        None
      """
      EXCEL_DIRECTORY = st.session_state.get('excel_directory')
      if file_pdf:
          file_name = f'{int(unique_n)}_{file_pdf.name}'
          with open(os.path.join(PDF_DIRECTROY, file_name),"wb") as f:
              f.write(file_pdf.getbuffer())

      ### GET MAX ROW ###
      schema = json.load(open(SCHEMA_TARGET))
      # st.write(schema)
      with open(EXCEL_DIRECTORY, mode='rb') as excel_file:
        wb = pd.read_excel(excel_file.read(),
                           sheet_name='Journal',
                          #  dtype=schema,
                           ).copy()
        max_row = len(wb)
        excel_file.close()

      df_dict = {}
      df_dict['Konto'] = [sel_account[:7]]
      df_dict['Art'] = [sel_account[:3]]
      df_dict['Spezifikation'] = [sel_account[4:7]]
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
          row_transformed.to_excel(writer,
                                   'Journal',
                                   startrow=max_row+1,
                                   header=False,
                                   index=False,
                                   )


  def validator(self, row):
          """Checks if row has been submitted to ExcelFile.
          If row is new:
          _____
          Returns:
          next row number for ExcelFile (int)"""
          EXCEL_DIRECTORY = st.session_state.get('excel_directory')
          wb = pd.read_excel(EXCEL_DIRECTORY, sheet_name='Journal')
          # validator column
          validator = list(wb.unique_identifier)
          uniqueness = ''.join(row.astype(str))
          if uniqueness in validator:
              return -999
          else:
              # return max internal reference number + 1
              max_n = wb['interne Ablage (NUR ZAHLEN)'].max() + 1
              if max_n == max_n:
                  return max_n
              else:
                  return 101
