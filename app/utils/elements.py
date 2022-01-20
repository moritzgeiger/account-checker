from io import BytesIO
import pandas as pd
import os
import json
config = json.load(open('app/config.json'))
dropdown = list(config.keys())
dropdown.insert(0, 'Choose Account')

def sidebar():
    file_csv = st.sidebar.file_uploader("Upload a CSV file.\nMust contain column 'Umsatz, Valuta, Buchungstag'",
                                type=([".csv"]))
    st.sidebar.title("Credits")
    st.sidebar.write("App made by Moritz Geiger. Visit my GitHub <a href='https://github.com/moritzgeiger/' target='blank'>here</a>.",
            unsafe_allow_html=True)
    st.sidebar.write(
        "Source code and notebook for this app can be found <a href='https://github.com/moritzgeiger/stockist' target='blank'>here</a>.",
        unsafe_allow_html=True)
    st.sidebar.markdown('**Note**\n\nComputation times can be slow due to reduced performance by Heroku.')

    return file_csv

def show_df(df_readable, index):
    st.write(df_readable.iloc[index])
    interval = st.selectbox('Choose account:', options=dropdown, key='interval')
    info = st.text_input("enter additional info.", key="info")
    file_pdf = st.file_uploader("Upload relevant PDF.",
                                type=([".pdf", ".PDF"]))
