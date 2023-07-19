import os
import requests
import json


def create_item(file_name):

    url = "https://api.monday.com/v2"

    payload1 = 'mutation { create_item (board_id: 1953569483, group_id: "new_group89026",'
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


def main():
    print('Starting Script')
    files = os.listdir('images')
    print("List of files in the Images Folder:", files)
    print("Total Files in the Images Folder:", len(files))
    for index, file in enumerate(files):
        file_name = file.split('.')[0]
        item_id = create_item(file_name)


if __name__ == '__main__':
    main()
