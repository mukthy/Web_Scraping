import os
import requests
import json


def create_item(file_name):

    url = "https://api.monday.com/v2"

    payload1 = 'mutation { create_item (board_id: 1953569483, group_id: "group_title",'
    payload2 = f'item_name: "{file_name}"'
    payload3 = ') { id }}'

    payload = payload1 + payload2 + payload3

    payload = json.dumps({
        'query': f'{payload}'
    })
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI0ODMyMTQ5MSwidWlkIjo0MTcwOTU3NywiaWFkIjoiMjAyMy0wMy0zMVQyMjoxNjo1MS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzUyNTA0NywicmduIjoidXNlMSJ9.wMkIJSQ8f9yRAwfXTNEJQ6xxuvxdNRXOGGasM9Ke5TY',
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    # print(response.text)  # un-comment while debugging.
    if response.status_code == 200:
        print('Item Creating...')
        item_id = response.json()['data']['create_item']['id']
        return item_id
    else:
        return None


def upload_files(file, item_id):
    print('Uploading File')

    # API URL
    url = "https://api.monday.com/v2/file"

    # item_id = '4242601503'
    # sample_payload = '''mutation add_file($file: File!) {add_file_to_column (item_id: 4242601503, column_id:"files" file: $file) {id name}}', 'map': '{"image":"variables.file"}'''

    # GraphQL Query

    p1 = 'mutation add_file($file: File!) {add_file_to_column (item_id: '
    p2 = f'{item_id}'
    p3 = ', column_id:"files" file: $file) {id name}}'

    # GraphQL Query Crafted
    payload = {'query': p1 + p2 + p3 + ' ', 'map': '{"video":"variables.file"}'}

    # print(payload)

    files = [('video', (f'{file}', open(f'/home/mukthy/Desktop/office/projects/upwork/nimrodmo_monday/videos/{file}', 'rb'), 'application/octet-stream'))]
    headers = {
        'Authorization': 'eyJhbGciOiJIUzI1NiJ9.eyJ0aWQiOjI0ODMyMTQ5MSwidWlkIjo0MTcwOTU3NywiaWFkIjoiMjAyMy0wMy0zMVQyMjoxNjo1MS4wMDBaIiwicGVyIjoibWU6d3JpdGUiLCJhY3RpZCI6NzUyNTA0NywicmduIjoidXNlMSJ9.wMkIJSQ8f9yRAwfXTNEJQ6xxuvxdNRXOGGasM9Ke5TY',
    }

    response = requests.request("POST", url, headers=headers, data=payload, files=files)

    # print(response.text)  # un-comment while debugging.

    if response.status_code == 200:
        return print(f'File {file} Uploaded Successfully.\n===========================================')
    else:
        return print(f'File {file} Upload Failed.\n===========================================')



def main():
    print('Starting Script')
    files = os.listdir('videos')
    print("List of files in the Images Folder:", files)
    print("Total Files in the Images Folder:", len(files))
    for index, file in enumerate(files):
        file_name = file.split('.')[0]
        item_id = create_item(file_name)
        if item_id is None:
            print("Item Creation Failed")
        else:
            print(f"Item Created with FileName '{file_name}' and ItemId is '{item_id}'.")
            upload_files(file, item_id)


if __name__ == '__main__':
    main()