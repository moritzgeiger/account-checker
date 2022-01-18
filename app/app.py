## GLOBAL LIBS ##
import streamlit as st
from io import BytesIO
import pandas as pd
import os
import json

## CUSTOM LIBS ##
from utils.elements import sidebar, show_df
# from utils.onedrive import OneDriveoperator
from utils.csv_parse import CSVHandler


########## PAGE CONFIG ##############
st.set_page_config(
    page_title="Stock Price Finder",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed")


file_pdf = None

############# SIDEBAR ################
file_csv = sidebar()

####### INDEX PAGE ########
st.title('Welcome to Account checker.')


####### HELPER ############
def clear_input():
    """Clears input after each iteration."""
    st.session_state["info"] = ""
    st.session_state["interval"] = "Choose Account"
    st.session_state["handle"] = "None"
    # file_pdf = None

####### ITEM PROCESSER ####
if 'row' not in st.session_state:
    st.write('Upload initial file in sidebar.')
    index = 0
    st.session_state['row'] = index

if file_csv:
    index = st.session_state['row']
    file = BytesIO(file_csv.getvalue())
    df = CSVHandler().parse(file)[0]
    len = len(df)
    df_readable = df.copy().astype(str)

    if st.session_state['row'] <= len:
        show_df(df_readable, index)

        handle = st.radio('Choose operation:', 
                         ('None', 'Process row', 'Skip row'), 
                         key='handle')

        if handle == 'Process row':
            st.session_state['row'] =  index + 1
            process = False
            if st.button('Next', on_click=clear_input):
                st.write('processing...')
        
        if handle == 'Skip row':
            st.session_state['row'] =  index + 1
            skip = False
            if st.button('Next', on_click=clear_input):
                st.write('skipping...')




