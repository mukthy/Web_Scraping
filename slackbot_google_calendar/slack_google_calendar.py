import datetime
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import render_template
import json
import requests
import threading
import validators
from flask import Flask, request, Response
import slack
from slack_sdk import WebClient
import create_events

# from slack import SlackClient

env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)

# client = slack.WebClient(token=os.environ['SLACK_TOKEN']) => For Old version of Slack-SDK
client = WebClient(token=os.environ["SLACK_TOKEN"])
# api = os.environ["APIKEY"]
# common webhook where the data will be posted to the bot directly and it will be visible to everyone.
slack_webhook_url = os.environ["SLACK_WEB_HOOK"]
headers = {
    "Content-type": "application/json",
}
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]


# slack_client = SlackClient(SLACK_BOT_TOKEN)


@app.route("/help", methods=["POST"])
def help_response():
    data = request.form
    text = data.get("text")
    validators.url(text)
    user = data.get("user_name")
    response_url = data["response_url"]
    message = {"text": "Connection successful!"}
    resp = requests.post(response_url, json=message)
    print(resp.status_code)
    help_event_thread = threading.Thread(target=help_event, args=(
        data, text, user, response_url, slack_webhook_url))
    help_event_thread.start()
    return "Processing, Please wait!!"


def help_event(data, text, user, response_url, slack_webhook_url):
    # print(response_url)
    print(response_url)
    print(data)
    print(user)

    event_data = {
        "text": "Usage of Bot",
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"@{user} Please enter the data in the follow format:\n /add-event <date>,<start_time>,<end_time>,<summary>,<email>,<timezone> \n\n Example: /add-event 2021-05-01,10:00,11:00,Patricia Wisdom,patricia@gmail.com,CST",
                },
            }
        ],
    }
    response = requests.post(
        url=response_url, headers=headers, data=json.dumps(
            event_data)
    )
    print(response.status_code)

    return Response(), 200


@app.route("/add-event", methods=["POST"])
def add_event_response():
    data = request.form
    text = data.get("text")
    validators.url(text)
    user = data.get("user_name")
    response_url = data["response_url"]
    message = {"text": "Connection successful!"}
    resp = requests.post(response_url, json=message)
    print(resp.status_code)
    x = threading.Thread(target=add_event, args=(
        data, text, user, response_url, slack_webhook_url))
    x.start()
    return "Processing, Please wait!!"


def add_event(data, text, user, response_url, slack_webhook_url):
    # print(response_url)
    print(response_url)
    print(data)
    print(user)

    if ', ' in text:
        text = text.replace(", ", ",")
    elif ' ,' in text:
        text = text.replace(" ,", ",")

    text = text.split(",")
    if len(text) == 6:
        date = text[0]
        start = text[1]
        end = text[2]
        summary = text[3]
        email = text[4]
        timezone = text[5]
        timezone = timezone.upper()

        create_event = create_events.main(summary, user, start, end, date, email, timezone)
        print(create_event)

        # create_event = json.loads(create_event)

        if create_event["status"] == "confirmed":
            data = {
                "Client Name": summary,
                "Artist Email": email,
                "Date": date,
                "Start Time": start,
                "End Time": end,
                "Timezone": timezone,
            }

            # data = str(data)
            # data = json.loads(data)
            data = json.dumps(data, indent=4)

            event_data = {
                "text": "Event Created Successfully",
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"@{user} Event Created Successfully with the details given below, please check your calendar.",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            # "text": f"Details: \n\n date: {data} \n\n start: {start} \n\n end: {end} \n\n Client: {summary} \n\n email: {email} \n\n timezone: {timezone}",
                            "text": f"Details: \n\n {data}",
                        },
                    },
                ],
            }
            response = requests.post(
                url=slack_webhook_url, headers=headers, data=json.dumps(
                    event_data)
            )
            print(response.status_code)

    else:
        event_data = {
            "text": "Event Creation Failed",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": f"@{user} Please enter the data in the follow format: /add-event <date>,<start_time>,<end_time>,<summary>,<email>,<timezone>",
                    },
                }
            ],
        }
        response = requests.post(
            url=response_url, headers=headers, data=json.dumps(
                event_data)
        )
        print(response.status_code)

    return Response(), 200


if __name__ == "__main__":
    app.run(port=5051, debug=True)
