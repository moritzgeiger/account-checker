## GLOBAL LIBS ##
import streamlit as st
from io import BytesIO
import pandas as pd
import os
import json

## CUSTOM LIBS ##
from utils.elements import sidebar, show_row, write_operation, iterator
# from utils.onedrive import OneDriveoperator
from utils.csv_parse import CSVHandler


########## PAGE CONFIG ##############
st.set_page_config(
    page_title="Account Checker",
    page_icon="💸",
    layout="centered",
    initial_sidebar_state="collapsed")


file_pdf = None

####### SIDEBAR ###########
file_csv = sidebar()

####### INDEX PAGE ########
st.title('Welcome to the Account Checker 🧾')

####### INIT PROCESSOR ####
if 'row' not in st.session_state:
    st.write('Upload initial file in sidebar.')
    index = 0
    st.session_state['row'] = index

####### ROW ITERATOR #######
st.write(file_csv)
_iterator = iterator(file_csv)

