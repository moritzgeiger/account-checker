import requests
import msal
import atexit
import os.path
import urllib.parse

TENANT_ID = '<your tenant id>'
CLIENT_ID = '<your app/client id>'
SHAREPOINT_HOST_NAME = '<your site name>.sharepoint.com'

AUTHORITY = 'https://login.microsoftonline.com/' + TENANT_ID
ENDPOINT = 'https://graph.microsoft.com/v1.0'

SCOPES = [
    'Files.ReadWrite.All',
    'Sites.ReadWrite.All',
    'User.Read',
    'User.ReadBasic.All'
]

cache = msal.SerializableTokenCache()

if os.path.exists('token_cache.bin'):
    cache.deserialize(open('token_cache.bin', 'r').read())

atexit.register(lambda: open('token_cache.bin', 'w').write(cache.serialize()) if cache.has_state_changed else None)

app = msal.PublicClientApplication(CLIENT_ID, authority=AUTHORITY, token_cache=cache)

accounts = app.get_accounts()
result = None
if len(accounts) > 0:
    result = app.acquire_token_silent(SCOPES, account=accounts[0])

if result is None:
    flow = app.initiate_device_flow(scopes=SCOPES)
    if 'user_code' not in flow:
        raise Exception('Failed to create device flow')

    print(flow['message'])

    result = app.acquire_token_by_device_flow(flow)

if 'access_token' in result:
    headers={'Authorization': 'Bearer ' + result['access_token']}

    folder = 'Test Folder'      # path in your OneDrive where file lives
    filename = 'Book.xlsx'      # the file you want to download

    # get the drive & file ID
    file_path = f'{folder}/{filename}'
    file_url = urllib.parse.quote(file_path)
    result = requests.get(f'{ENDPOINT}/me/drive/root:/{file_url}', headers=headers)
    result.raise_for_status()
    json = result.json()
    drive_id = json['parentReference']['driveId']
    file_id = json['id']

    # download the file
    result = requests.get(f'{ENDPOINT}/drives/{drive_id}/items/{file_id}/content', headers=headers)
    open('Book.xlsx', 'wb').write(result.content)

else:
    raise Exception('no access token in result')