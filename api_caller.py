import googleapiclient.discovery
import googleapiclient
from google.oauth2 import service_account
import json
SERVICE_ACCOUNT_FILE = 'service-account-test-domain.json'
SAMPLE = {
            'id': '0AO3KVCL7ImPEUk9PVA',
            'name': 'Test 1',
            'kind': 'drive#permissionList',
            'permissions': [{'kind': 'drive#permission', 'id': '09302626123764563415', 'type': 'user', 'role': 'organizer'},
                            {'kind': 'drive#permission', 'id': '12427817091976751831', 'type': 'user', 'role': 'organizer'}]
            }


def api_caller(scope=['https://www.googleapis.com/auth/drive.readonly']):
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=scope)
    delegated_credentials = credentials.with_subject('sedthakit.pra@test.truedigital.com')

    result = googleapiclient.discovery.build('drive', 'v3', credentials=delegated_credentials)

    return result


def get_user(drivewithpermission=None):
    share_permission = {}

    if drivewithpermission is None:
        drivewithpermission = SAMPLE
    
    share_permission.update({'share_name': drivewithpermission['name'],'permissions': []})
    
    credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=['https://www.googleapis.com/auth/drive.readonly'])
    delegated_credentials = credentials.with_subject('sedthakit.pra@test.truedigital.com')

    permissionlist = googleapiclient.discovery.build('drive', 'v2', credentials=delegated_credentials)

    for each_user in drivewithpermission['permissions']:
        result = permissionlist.permissions().get(fileId=drivewithpermission['id'], permissionId=each_user['id'], supportsAllDrives=True, useDomainAdminAccess=True).execute()
        print(drivewithpermission['name'])
        # cleanup unwanted element
        del result['kind']
        del result['etag']
        del result['selfLink']
        del result['emailAddress']
        del result['domain']
        del result['id']
        print(json.dumps(result, indent=4))
        share_permission['permissions'].append(result)

    return share_permission

def debug():
    # result = api_caller()
    # print(result.drives().list(useDomainAdminAccess=True).execute())

    result = get_user()
    print(result)


if __name__ == '__main__':
    debug()
