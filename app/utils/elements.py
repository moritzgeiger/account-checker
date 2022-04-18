from io import BytesIO
import pandas as pd
import os
import json
import streamlit as st
from utils.csv_parse import CSVHandler
# from utils.onedrive import OneDriveOperator
from utils.excel_writer import ExcelWriter
from utils.zipper import zipper
from utils.purge_temps import purge_temps


### CONFIGS ###
config = json.load(open('config.json'))
dropdown = list(config.keys())
dropdown.insert(0, 'Choose Account')
csv_handler = CSVHandler()
excel_handler = ExcelWriter()
REDIRECT_URI = os.environ.get('REDIRECT_URI', 'http://localhost:8501/')

def sidebar():

    file_xlsx = st.sidebar.file_uploader("Upload your target Excel file.",
                                type=([".xlsx"]), key='output_file')
    st.sidebar.markdown("[Check schema requirements](https://raw.githubusercontent.com/moritzgeiger/account-check/master/static/schema_output.png)")

    if file_xlsx and not st.session_state.get('excel_directory'):
        excel_directory = 'temp/cur_file.xlsx'
        with open(excel_directory, "wb") as f:
            f.write(file_xlsx.getbuffer())
            f.close()
        st.session_state['excel_directory'] = excel_directory

    st.sidebar.write("SOURCE FILE")
    file_csv = st.sidebar.file_uploader("Upload a CSV file.\nFirst column must be 'Buchungstag'",
                            type=([".csv"]), key='input_file')
    if file_csv:
        jump_row = st.sidebar.text_input("Jump to row (starts with 0):", key="jump")
        if st.sidebar.button('Jump'):
            st.session_state['row'] =  int(jump_row)

    st.sidebar.write('---')

    output_dir = 'temp/'
    zip_filename = 'journal_output.zip'

    if st.session_state.get('excel_directory'):

        finish = st.sidebar.button(
              label='Finish work',
        )
        if finish:
          s = zipper(
                zip_filename=zip_filename,
                source_path=output_dir,
          )
          dl_button = st.sidebar.download_button(
                label='Download file',
                data=s.getvalue(),
                file_name=zip_filename,
                )

    delete = st.sidebar.button(
        label='Clear temp folders',
    )
    if delete:
        _ = purge_temps()
        st.sidebar.write('temp/ folder emptied.')

    st.sidebar.title("Credits")
    st.sidebar.write("App made by Moritz Geiger. Visit my GitHub <a href='https://github.com/moritzgeiger/' target='blank'>here</a>.",
            unsafe_allow_html=True)
    st.sidebar.write(
        "Source code and notebook for this app can be found <a href='https://github.com/moritzgeiger/account-checker' target='blank'>here</a>.",
        unsafe_allow_html=True)
    st.sidebar.markdown('**Note**\n\nComputation times can be slow due to reduced performance Cloud Run.')

    return file_csv


def write_operation(handle=None, row_process=None, sel_account=None, input=None, file_pdf=None, unique_n=None):
    """Clears input after each iteration."""
    st.session_state["input"] = ""
    st.session_state["interval"] = "Choose Account"
    st.session_state["handle"] = "None"
    index = st.session_state['row']
    st.session_state['row'] =  index + 1
    if handle:
        _saver = excel_handler.save_row(row_process, sel_account, input, file_pdf, unique_n)


def show_row(row):
    st.write(row)
    sel_account = st.selectbox('Choose account:', options=dropdown, key='interval')
    input = st.text_input("enter additional info.", key="input")
    file_pdf = st.file_uploader("Upload relevant PDF.",
                                type=([".pdf", ".PDF"]), key="file_pdf")

    return sel_account, input, file_pdf

def iterator(file_csv):
    if file_csv:
        index = st.session_state['row']
        file = BytesIO(file_csv.getvalue())
        df = csv_handler.parse(file)
        len = df.shape[0]
        df_readable = df.copy().astype(str)

        if st.session_state['row'] <= len:
            row = df_readable.iloc[index]
            row_process = df.iloc[index]
            # show row and instantiate user inputs
            sel_account, input, file_pdf = show_row(row)
            unique_n = excel_handler.validator(row_process)
            if unique_n == -999:
                st.warning('Ooops, looks like you have saved that row already. Skip this one.')

            ## Handler radio
            handle = st.radio('Choose operation:',
                            ('None', 'Process row', 'Skip row'),
                            key='handle')

            if handle == 'Process row':
                if input == '':
                    st.warning('It is recommended to add some description to the row.')

                if sel_account == 'Choose Account':
                    st.error('Please choose account first.')
                    process = False

                else:
                    if st.button('Next',
                                on_click=write_operation,
                                kwargs={'handle': handle,
                                'row_process': row_process,
                                'sel_account': sel_account,
                                'input': input,
                                'file_pdf': file_pdf,
                                'unique_n':unique_n if file_pdf else None},
                                ):
                        st.write('processing...')

            if handle == 'Skip row':
                skip = False
                if st.button('Next', on_click=write_operation):
                    st.write('skipping...')
