from io import BytesIO
import pandas as pd
import os
import json
import streamlit as st
from utils.csv_parse import CSVHandler
from utils.onedrive import OneDriveOperator


### CONFIGS ###
config = json.load(open('app/config.json'))
dropdown = list(config.keys())
dropdown.insert(0, 'Choose Account')
csv_handler = CSVHandler()
 
def sidebar():
    one_drive_client = OneDriveOperator()

    code = st.experimental_get_query_params().get('code')
    if code:
        st.session_state['code'] = code
        token = one_drive_client.authenticate(st.session_state['code'][0])
        if not st.session_state.get('token'):
            st.session_state['token'] = token
        if st.session_state.get('token') and not st.session_state.get('folders'):
            folders = one_drive_client.choose_folder(st.session_state.get('token'))
            st.session_state['folders'] = folders
        else:
            try:
                login_url = one_drive_client.login_link()
                st.sidebar.write(f"Please log in to your OneDrive:")
                st.sidebar.write(f"[LOGIN]({login_url})")
                st.sidebar.markdown('---')
            except Exception as e:
                st.sidebar.error(f"Could not generate login link.\n Check your internet connection.")
                st.sidebar.error(f"{e}")


    if st.session_state.get('is_logged') and st.session_state.get('folders'):
        st.sidebar.write('You are logged in.')
        folders = dict(st.session_state.get('folders'))
        folder_keys = ['Choose folder'] + list(folders.keys()) 
        sel_folder = st.sidebar.selectbox('Choose folder:', options=folder_keys)
        folder_id = folders.get(sel_folder)
        st.sidebar.markdown('---')
    else:
        st.write('naa')

    

    

    


    

    file_csv = st.sidebar.file_uploader("Upload a CSV file.\nFirst column must be 'Buchungstag'",
                                type=([".csv"]), key='input_file')
    if file_csv:
        jump_row = st.sidebar.text_input("Jump to row (starts with 0):", key="jump")
        if st.sidebar.button('Jump'):
            st.session_state['row'] =  int(jump_row)
            

    

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
        _saver = csv_handler.save_row(row_process, sel_account, input, file_pdf, unique_n)
        

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
            unique_n = csv_handler.validator(row_process)
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
                                'unique_n':unique_n},
                                ):
                        st.write('processing...')
            
            if handle == 'Skip row':
                skip = False
                if st.button('Next', on_click=write_operation):
                    st.write('skipping...')