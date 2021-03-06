from azure.identity import InteractiveBrowserCredential
from msgraph.core import GraphClient
from configparser import ConfigParser
# from ms_graph.clientimport import MicrosoftGraphClient
from dotenv import load_dotenv, find_dotenv
import msal
import urllib
import requests
import os
import streamlit as st

load_dotenv(find_dotenv())

TENANT_ID = os.environ.get('TENANT_ID')
CLIENT_ID = os.environ.get('CLIENT_ID')
AUTHORITY = os.environ.get('AUTHORITY') + TENANT_ID
ENDPOINT = os.environ.get('ENDPOINT')
CLIENT_ID = os.environ.get('CLIENT_ID')
REDIRECT_URI = os.environ.get('REDIRECT_URI', 'http://localhost:8501/')

client_secret = os.environ.get('client_secret')


RESOURCE = "https://graph.microsoft.com/"
AUTHORITY_URL = "https://login.microsoftonline.com/"
AUTH_ENDPOINT = "/oauth2/v2.0/authorize?"
TOKEN_ENDPOINT = "/oauth2/v2.0/token"
account_type = 'common'



SCOPES = [
    'Files.ReadWrite.All',
    'Sites.ReadWrite.All',
    'User.Read',
    'User.ReadBasic.All'
]

class OneDriveOperator():
    def __init__(self):
        try:
            self.client_app = msal.ConfidentialClientApplication(
                    client_id=CLIENT_ID,
                    authority=AUTHORITY_URL + account_type,
                    client_credential=client_secret,
                )
        except:
            st.error("Couldn't connect to OneDrive. Try again later.")


    def login_link(self):
        graph_url = AUTHORITY_URL + account_type + AUTH_ENDPOINT

        try:
            auth_url = self.client_app.get_authorization_request_url(scopes=SCOPES,
                                                            state='ABC',
                                                            redirect_uri=REDIRECT_URI)
        except:
            st.error("Couldn't create Login Link. Try again later.")
        return auth_url



    def authenticate(self, code):
        token_dict = self.client_app.acquire_token_by_authorization_code(
                            code=code,
                            scopes=SCOPES,
                            redirect_uri=REDIRECT_URI)
        try:
            st.session_state['is_logged'] = True
            return token_dict.get('access_token')
        except Exception as e:
            st.error('Authentication with OneDrive failed.')


    def find_folders(self, token):
        headers={'Authorization': 'Bearer ' + token}
        params={'allowexternal': 'true'}

        # get the driveD
        result_drive = requests.get(f'{ENDPOINT}/me/drives', headers=headers, params=params)
        drive_id = result_drive.json().get('value')[0].get('id')

        # show folders
        result = requests.get(f'{ENDPOINT}/drives/{drive_id}/root/children', headers=headers, params=params)
        return result.json()

    def choose_folder(self, token):
        result = self.find_folders(token)
        avail_folders = {val.get('name'): val.get('id') for val in result.get('value')}

        return avail_folders

    def choose_file(self, item_id, token):

        headers={'Authorization': 'Bearer ' + token}
        params={'allowexternal': 'true'}
        result = requests.get(f'{ENDPOINT}/me/drive/items/{item_id}', headers=headers, params=params)
        return result.content

    def add_row(self):
        pass
