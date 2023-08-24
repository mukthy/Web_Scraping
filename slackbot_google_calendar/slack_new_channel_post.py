import os
from pathlib import Path
from dotenv import load_dotenv
import json
import requests
import time
from datetime import datetime
from slack_sdk import WebClient


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

client = WebClient(token=os.environ["SLACK_USER_TOKEN"])

headers = {
    "Content-type": "application/json",
}
SLACK_USER_TOKEN = os.environ["SLACK_USER_TOKEN"]


def fetch_channels():

    url = "https://slack.com/api/conversations.list?limit=1000&types=private_channel%2Cpublic_channel&pretty=1"

    payload = {}
    headers = {
        'Authorization': f'Bearer {SLACK_USER_TOKEN}'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    response = json.loads(response.text)
    channels = response['channels']

    channel_list = []

    for channel in channels:
        channel_id = channel['id']
        channel_name = channel['name']
        channel_created = channel['created']

        channel_list.append({
            'channel_id': channel_id,
            'channel_name': channel_name,
            'channel_created': channel_created
        })

    # pprint.pprint(channel_list)

    return channel_list


def check_creation_date(channel_list):
    recently_created_channel_list = []
    for channel in channel_list:
        channel_created = channel['channel_created']
        current_time_utc = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        converted_created_time = time.gmtime(channel_created)
        converted_created_time = time.strftime("%Y-%m-%d %H:%M:%S", converted_created_time)
        time_diff = (datetime.strptime(current_time_utc, '%Y-%m-%d %H:%M:%S') - datetime.strptime(converted_created_time, '%Y-%m-%d %H:%M:%S')).total_seconds()
        time_diff = time_diff / 60
        # print(time_diff)
        if time_diff < 5:
            print("Time Difference: ", time_diff)
            # print('Channel Created Recently')
            # print(channel['channel_name'])
            # print(channel['channel_id'])
            recently_created_channel_list.append(channel['channel_id'])

    return recently_created_channel_list


def send_message_to_channel(channel_id):

    response = client.chat_meMessage(
        channel=channel_id, mrkdwn=False, parse='full',
        text='''
Client Contact:
Allergies: n/a
Vendors:

Lead Hairstylist: TBD
Lead Makeup Artist: TBD

----------

Trial/Rehearsal Dinner {Date} (ready by )
(photo/video of each client are required to be uploaded below)

Lead Hairstylist @ for hair
Lead Makeup Artist @ for makeup

Location:
Tower: TBD Room: TBD

Venue Access: Call client directly, so they can meet you at the first floor elevators of the tower.

Gate Code:


----------

Wedding {Date} (ready by )
(photo/video of each client are required to be uploaded below)

Lead Hairstylist @ for hair
Lead Makeup Artist @ for makeup

Location:
Tower: TBD Room: TBD

Venue Access: Call client directly, so they can meet you at the first floor elevators of the tower.

Gate Code:'''
    )
    print(response)


def main():
    channel_list = fetch_channels()
    recently_created_channel_list = check_creation_date(channel_list)
    if len(recently_created_channel_list) > 0:
        print("Recently Created Channel ID: ", recently_created_channel_list)

        for channel_id in recently_created_channel_list:
            send_message_to_channel(channel_id)
            print("Message Sent to Channel: ", channel_id)
    else:
        print("No Recently Created Channel Found")


if __name__ == "__main__":
    main()
