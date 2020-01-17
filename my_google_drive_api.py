import query_parsing
import api_caller
import json
import pandas as pd

QUERY_TERM = ''

drive = api_caller.api_caller()
response = drive.drives().list(useDomainAdminAccess=True, q=QUERY_TERM).execute()

print(json.dumps(response))
# get the permission for each share drive and put it into excel

share_list = query_parsing.share_drive_parsing(response['drives'])

#Excel Writer
writer = pd.ExcelWriter('Share_drive_permission.xlsx', engine='xlsxwriter')

for each_share in share_list:
    permission_list = drive.permissions().list(fileId=each_share['id'], useDomainAdminAccess=True, supportsAllDrives=True).execute()
    each_share.update(permission_list)
    print(f"the permission of {each_share['name']},{each_share['id']} is {permission_list['permissions']}")
    print(each_share)
    print()
    result = api_caller.get_user(each_share)
    print(result)
    df = pd.DataFrame(result['permissions'])
    df.to_excel(writer, sheet_name=result['share_name'])
    # userlist = api_caller.get_user(permission_list)

writer.save()

