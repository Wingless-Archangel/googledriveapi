def share_drive_parsing(some_result):
    drive_list = []

    for element in some_result:
        # drive_list.update({element['name']: element['id']})
        del element['kind']
        drive_list.append(element)

    return drive_list

def debug():
    TEST_DATA = [{'kind': 'drive#drive', 'id': '0AO3KVCL7ImPEUk9PVA', 'name': 'Test 1'},
                 {'kind': 'drive#drive', 'id': '0AL3kj3ctBxA4Uk9PVA', 'name': 'Test 2'}]
    result = share_drive_parsing(TEST_DATA)
    print(result)




if __name__ == '__main__':
    debug()
