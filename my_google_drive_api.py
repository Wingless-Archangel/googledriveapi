import pandas as pd

import api_caller
import query_parsing

QUERY_TERM = ''
nextPageToken = None
share_list = []

drive = api_caller.api_caller()

while True:
    response = drive.drives().list(pageToken=nextPageToken, useDomainAdminAccess=True, q=QUERY_TERM).execute()

    # print(json.dumps(response))
    # get the permission for each share drive and put it into excel
    share_list += query_parsing.share_drive_parsing(response['drives'])

    if 'nextPageToken' not in response:
        break

    nextPageToken = response['nextPageToken']

# Excel Writer
writer = pd.ExcelWriter('Share_drive_permission.xlsx', engine='xlsxwriter')

for each_share in share_list:
    permission_list = drive.permissions().list(fileId=each_share['id'], useDomainAdminAccess=True, supportsAllDrives=True).execute()
    each_share.update(permission_list)
    result = api_caller.get_user(each_share)

    df = pd.DataFrame(result['permissions'])
    sheetname = result['share_name']

    if len(sheetname) > 31:
        sheetname = sheetname[:31]

    df.to_excel(writer, sheet_name=sheetname)

writer.save()

