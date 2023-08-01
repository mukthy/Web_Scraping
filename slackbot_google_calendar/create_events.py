from datetime import datetime, timedelta
from cal_setup import get_calendar_service


def main(text, user, start, end, date, email, timezone):
    # creates one hour event tomorrow 10 AM IST
    service = get_calendar_service()

    # date = input("Enter date in YYYY-MM-DD format: ")
    d = datetime.strptime(date, "%Y-%m-%d").date()
    # start_time = input("Enter start time in HH:MM format: ")
    # end_time = input("Enter end time in HH:MM format: ")
    start = datetime(d.year, d.month, d.day, int(start.split(":")[0]), int(start.split(":")[1])).isoformat()
    end = datetime(d.year, d.month, d.day, int(end.split(":")[0]), int(end.split(":")[1])).isoformat()
    print(start)
    print(end)

    # d = datetime.now().date()
    # tomorrow = datetime(d.year, d.month, d.day, 10) + timedelta(days=1)
    # start = tomorrow.isoformat()
    # end = (tomorrow + timedelta(hours=1)).isoformat()

    event_result = service.events().insert(calendarId='primary',
                                           body={
                                               "summary": f'Ruby Finch - {text}',
                                               "description": f'Ruby Finch - {text}',
                                               "start": {"dateTime": start, "timeZone": f'{timezone}'},
                                               "end": {"dateTime": end, "timeZone": f'{timezone}'},
                                               "attendees": [{"email": f"{email}"}]
                                           }
                                           ).execute()

    print("created event")
    print("id: ", event_result['id'])
    print("summary: ", event_result['summary'])
    print("starts at: ", event_result['start']['dateTime'])
    print("ends at: ", event_result['end']['dateTime'])

    return event_result


if __name__ == '__main__':
    main()
