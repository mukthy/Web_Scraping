import datetime
from cal_setup import get_calendar_service
import pprint
from pathlib import Path
from dotenv import load_dotenv
import os
import json

env_path = Path(".") / ".env"
print(env_path)
load_dotenv(dotenv_path=env_path)

calender_id = os.environ["CALENDARID"]


def main():
    service = get_calendar_service()
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
    print(now)
    print('Getting List o 10 events')

    events_result = service.events().list(
        calendarId=f'{calender_id}', timeMin=now,
        maxResults=2, singleEvents=True,
        orderBy='startTime').execute()
    # pprint.pprint(events_result)
    events = events_result.get('items', [])
    # pprint.pprint(events)
    pprint.pprint(len(events))

    email = []
    details = {}
    for event in range(len(events)):
        # print(events[event]['start']['date'], events[event]['creator']['email'])
        # pprint.pprint(events[event])

        if 'attendees' in events[event]:

            if events[event]['attendees'][0]['email'] == f'{calender_id}':
                print(events[event]['attendees'][1]['email'])
                print(events[event]['summary'])
                # email.append(events[event]['attendees'][1]['email'])
                details[events[event]['attendees'][1]['email']] = events[event]['summary']
                # return events[event]['attendees'][1]['email']
            else:
                print(events[event]['attendees'][0]['email'])
                print(events[event]['summary'])
                # email.append(events[event]['attendees'][0]['email'])
                details[events[event]['attendees'][0]['email']] = events[event]['summary']
                # return events[event]['attendees'][0]['email']

        else:
            print(events[event]['creator']['email'])
            print(events[event]['summary'])
            # email.append(events[event]['creator']['email'])
            details[events[event]['creator']['email']] = events[event]['summary']
            # return events[event]['creator']['email']
    # print(details)
    return details


if __name__ == '__main__':
    main()