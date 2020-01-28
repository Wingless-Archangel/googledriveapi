import json

import googleapiclient
import googleapiclient.discovery
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'service-account-real-domain.json'
SAMPLE = {
            'id': '0AO3KVCL7ImPEUk9PVA',
            'name': 'Test 1',
            'kind': 'drive#permissionList',
            'permissions': [{'kind': 'drive#permission', 'id': '09302626123764563415', 'type': 'user', 'role': 'organizer'},
                            {'kind': 'drive#permission', 'id': '12427817091976751831', 'type': 'user', 'role': 'organizer'}]
            }


def api_caller(scope=None, pageToken=None):
    if scope is None:
        scope = ['https://www.googleapis.com/auth/drive.readonly']

    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
    delegated_credentials = credentials.with_subject('admin@truedigital.com')
    result = googleapiclient.discovery.build('drive', 'v3', credentials=delegated_credentials)

    return result


def get_user(drivewithpermission=None, pageToken=None):
    share_permission = {}
    nextPageToken = None

    if drivewithpermission is None:
        drivewithpermission = SAMPLE
    
    share_permission.update({'share_name': drivewithpermission['name'],'permissions': []})
    
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    delegated_credentials = credentials.with_subject('admin@truedigital.com')

    permissionlist = googleapiclient.discovery.build('drive', 'v2', credentials=delegated_credentials)

    for each_user in drivewithpermission['permissions']:
        result = permissionlist.permissions().get(fileId=drivewithpermission['id'], permissionId=each_user['id'], supportsAllDrives=True, useDomainAdminAccess=True).execute()
        # cleanup unwanted element
        del result['kind']
        del result['etag']
        del result['selfLink']
        del result['emailAddress']
        del result['domain']
        del result['id']
        share_permission['permissions'].append(result)

    return share_permission


def debug():
    nextPageToken = None
    while True:
        response = api_caller()
        result = response.drives().list(pageToken=nextPageToken, useDomainAdminAccess=True).execute()
        print(f"nextPageToken is {result['nextPageToken']}")
        print(json.dumps(result['drives'], indent=4))

        if 'nextPageToken' not in result:
            break

        nextPageToken = result['nextPageToken']

    # result = get_user()
    # print(result)


if __name__ == '__main__':
    debug()
