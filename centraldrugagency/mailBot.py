import time
from datetime import datetime
import json
import os

import requests
from pathlib import Path
from dotenv import load_dotenv
import pprint

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)
# client = WebClient(token=os.environ["SLACK_TOKEN"])

slack_user_token = os.getenv("SLACK_USER_TOKEN")
slack_bot_token = os.getenv("SLACK_BOT_TOKEN")



def get_messages():
    url = "https://slack.com/api/conversations.history?channel=C05FKMMJNKE&pretty=1&limit=30"

    payload = {}
    headers = {"Authorization": "Bearer " + slack_user_token}

    response = requests.request("GET", url, headers=headers, data=payload)

    # pprint.pprint(response.json())

    messages = response.json()["messages"]

    list_of_details = []

    for message in messages:
        # pprint.pprint(message)
        if "files" in message:
            for file in message["files"]:
                created_time = file["created"]
                name = file["name"]
                from_user = file["from"][0]["address"]
                # file_link = file["attachments"][0]["url"]
                try:
                    file_link = file["attachments"][0]["url"]
                except IndexError:
                    file_link = file["url_private_download"]

                preview = file["plain_text"]

                details = {
                    "Created": created_time,
                    "Name": name,
                    "from_user": from_user,
                    "file_link": file_link,
                    "Subject": preview,
                }

                list_of_details.append(details)

            else:
                pass

                # print("--------------------------------------------------")
                # pprint.pprint(details)
                # print("--------------------------------------------------")

    return list_of_details


def main():
    details = get_messages()
if __name__ == "__main__":
    main()
