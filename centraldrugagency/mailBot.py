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


def post_slack(detail):
    slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL")
    channel = "C05FREWS7PH"
    print("Downloading files To local")

    file_name = detail["file_link"].split("/")[-1]
    print(file_name)

    payload = {}
    headers = {
        'authority': 'files-origin.slack.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
        'cookie': '_rdt_uuid=1672436977974.53f9f26b-705c-4606-b34e-97a50006af14; _cs_c=1; __adroll_fpc=3c4a87f5d893a75f718d522f2d1e04d0-1672437261426; __qca=P0-714863048-1672437260907; _lc2_fpi=e00b11ac9c9b--01gnjgetf7cqyp2d3qfhxca7dr; b=.82b8a19151bb35cde45eaf7d43ea547a; shown_ssb_redirect_page=1; shown_download_ssb_modal=1; show_download_ssb_banner=1; no_download_ssb_banner=1; ssb_instance_id=766dcc4e-3653-45a9-a94c-c6c73609f87e; d=xoxd-GLcZkaaFAtVgfg0lff4W1FqH7TE36f0T%2FJiIvkoeMaA2Mupi7epKoqtCYl17etp303OWvxm6o6x6pKKYCLWWYvyQH39bFmkb%2FGgxasnvCShMecRpcJ3kQKFa2EeBPNT%2FllfAWim6h4KUR5E6PhAerK4aNQ6Htc0Bf7BM0cvYBqQ%2Bin4hkTpajuzrFw%3D%3D; d-s=1688244735; _li_dcdm_c=.slack.com; _gcl_au=1.1.1742396543.1688499413; _fbp=fb.1.1688588527536.645896527; _ga=GA1.1.220146085.1672436978; __ar_v4=4UHU5P4P3FESHLUMNBLWAU%3A20230704%3A3%7CQCM34G7NBZEHHATIFDIUBJ%3A20230704%3A3%7CK2HN2U4VSJGOVKC2WJLQNH%3A20230704%3A3; utm=%7B%22utm_source%22%3A%22in-prod%22%2C%22utm_medium%22%3A%22inprod-link_app_settings-user_card-click%22%7D; x=82b8a19151bb35cde45eaf7d43ea547a.1689025132; _cs_mk_ga=0.8305882080386808_1689025241715; PageCount=6; _cs_cvars=%7B%221%22%3A%5B%22Visitor%20ID%22%2C%22.82b8a19151bb35cde45eaf7d43ea547a%22%5D%2C%222%22%3A%5B%22Is%20Signed%20In%22%2C%22true%22%5D%2C%223%22%3A%5B%22URL%20Path%22%2C%22%2Foauth%22%5D%2C%224%22%3A%5B%22Visitor%20Type%22%2C%22customer%22%5D%7D; _cs_id=ebe519f1-2e87-acc2-b525-d32efafe3c13.1672437260.29.1689025389.1689025389.1.1706601260866; _cs_s=1.0.0.1689027189770; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Jul+11+2023+03%3A13%3A24+GMT%2B0530+(India+Standard+Time)&version=202211.1.0&isIABGlobal=false&hosts=&consentId=91df7a2c-e906-44f9-940b-cf1305894b7e&interactionCount=1&landingPath=NotLandingPage&groups=1%3A1%2C3%3A1%2C2%3A1%2C4%3A1&AwaitingReconsent=false; _ga_QTJQME5M5D=GS1.1.1689025242.30.1.1689025404.8.0.0',
        'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    }
    # headers = {
    #     'authority': 'files-origin.slack.com',
    #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    #     'cache-control': 'no-cache',
    #     'cookie': 'b=a54cd944e035b52cca2fe574f8b093ee; d=xoxd-As7icTUQpRje%2BdcNkbXiciXzvr0GevS1Gc%2Fx5vLTksk%2BK5%2B6pxKUe0ycw8oWcUiw0Uom22YOqaxdOzl2brheZtEQ9%2FewrX0rzfQuoVs37CHrBVYIetYsyZ95Q4IaawmSAHN5OiZuVP8EO5v09z%2F5VCN9c3bVLuFgS8po3xIRDzDOpEUk8QucfUhi7w%3D%3D; d-s=1688926079; lc=1688926079; tz=330; ssb_instance_id=7d04f9a4-5446-4a95-8efa-08bf0a3a40be; shown_ssb_redirect_page=1',
    #     'pragma': 'no-cache',
    #     'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Brave";v="114"',
    #     'sec-ch-ua-mobile': '?0',
    #     'sec-ch-ua-platform': '"macOS"',
    #     'sec-fetch-dest': 'document',
    #     'sec-fetch-mode': 'navigate',
    #     'sec-fetch-site': 'none',
    #     'sec-fetch-user': '?1',
    #     'sec-gpc': '1',
    #     'upgrade-insecure-requests': '1',
    #     'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
    # }

    file_download = requests.request("GET", url=detail["file_link"], headers=headers, data=payload)

    with open(f'/Users/mukthy/Desktop/office/projects/upwork/centraldrugagency/files/{file_name}', "wb") as f:
        f.write(file_download.content)

    print("Sending Slack Message")

    headers = {
        "Content-type": "application/json",
    }

    name = detail["Name"].lower()
    name = name.replace(" ", "-")
    name = name.replace(" - ", "-")

    if ("audit" in name) or ("audit-reports" in name):
        print("Sending Slack Message to Audit")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_AUDIT")
        channel = "C04UKH9TW5T"

    elif ("cash" in name) or ("cash-handover-detail" in name):
        print("Sending Slack Message to Cash")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_CASH")
        channel = "C04SM5SNBQW"

    elif ("exceptions" in name) or ("exceptions-summary-report" in name) or ("exception" in name) or ("exception-summary" in name) or ("exception-summary-report" in name):
        print("Sending Slack Message to Exceptions")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_EXCEPTIONS")
        channel = "C05F43T6GP9"

    elif ("modified" in name) or ("modified-transactions" in name):
        print("Sending Slack Message to Transactions")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_TRANSACTIONS")
        channel = "C05G5T8GPEF"

    elif ("pdc" in name) or ("pdc-detailed-report" in name):
        print("Sending Slack Message to PDC")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_PDC")
        channel = "C04UZNFTVK9"

    elif ("pending-items" in name) or ("pending-items-in-ipo" in name):
        print("Sending Slack Message to IPO")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_PENDING_ITEMS")
        channel = "C04V0T01TG9"

    elif ("pending-po" in name) or ("pending-po-summary" in name):
        print("Sending Slack Message to PO")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_PENDING_PO")
        channel = "C04U7A7CFNU"

    elif ("counterwise" in name) or ("sales-salesrn-counterwise" in name):
        print("Sending Slack Message to Counterwise")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_COUNTERWISE")
        channel = "C05FNHAP22Y"

    elif ("tenderwise" in name) or ("sales-salesrn-tenderwise" in name):
        print("Sending Slack Message to Tenderwise")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_TENDERWISE")
        channel = "C04UQBRCVMJ"

    elif ("supplier" in name) or ("supplier-outstanding" in name) or ("supplier-outstanding-summary" in name):
        print("Sending Slack Message to Outstanding")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_OUTSTANDING")
        channel = "C04UJMKT8UV"

    elif ("void" in name) or ("void-invoice" in name) or ("void-invoice-details" in name):
        print("Sending Slack Message to Void Invoice")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_VOID")
        channel = "C05FKM9470S"

    elif ("negative" in name) or ("negative-margin" in name) or ("negative-margin-itemwise" in name):
        print("Sending Slack Message to negative-margin-itemwise")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_VOID")
        channel = "C05GC5NTGFL"

    elif ("sales" in name) or ("sales-register" in name) or ("sales-register-datewise" in name):
        print("Sending Slack Message to sales-register-datewise")
        slack_webhook_url = os.getenv("SLACK_WEBHOOK_URL_VOID")
        channel = "C05G35XM1B8"

    try:
        subject = detail["Subject"].split(detail["Name"])[1]
        if len(subject) == 0:
            subject = detail["Subject"]
    except IndexError:
        subject = detail["Subject"]

    stripped_details = {
        "Name": detail["Name"],
        "Subject": subject
    }

    # stripped_details = json.dumps(stripped_details, indent=4)

    # event_data = {
    #     "text": "Mail Posted",
    #     "blocks": [
    #         {
    #             "type": "section",
    #             "text": {
    #                 "type": "mrkdwn",
    #                 "text": f"Mail Details: \n\n{stripped_details} \n\n Email Attachment File Below.",
    #             },
    #         },
    #     ],
    # }
    #
    # response = requests.post(
    #     url=slack_webhook_url, headers=headers, data=json.dumps(event_data)
    # )
    # print(response.status_code)

    print("Uploading file to slack")

    file_upload_url = "https://slack.com/api/files.upload"

    name = stripped_details["Name"]
    subject = stripped_details["Subject"]

    payload = {'initial_comment': f'Name: {name} \n\nSubject: {subject}',
               'channels': f'{channel}'}

    full_file_path = f'/Users/mukthy/Desktop/office/projects/upwork/centraldrugagency/files/{file_name}'

    if file_name.endswith(".html"):
        files = [
            ('file', (f'{file_name}',
                      open(f'{full_file_path}', 'rb'),
                      'text/html'))
        ]
    else:

        files = [
            ('file', (f'{file_name}',
                      open(f'{full_file_path}', 'rb'),
                      'application/vnd.ms-excel'))
        ]
    headers = {
        'Authorization': 'Bearer ' + slack_bot_token
    }

    response = requests.request("POST", url=file_upload_url, headers=headers, data=payload, files=files)

    print(response.text)

    print("Deleting file from local")
    os.remove(f'/Users/mukthy/Desktop/office/projects/upwork/centraldrugagency/files/{file_name}')


def main():
    details = get_messages()
    print("=====================================================")
    current_time = datetime.utcnow()
    current_time = current_time.strftime("%Y-%m-%d %H:%M:%S")
    print(f"Current Time: {current_time}")

    for detail in details:
        created_time = detail["Created"]
        created_time = time.gmtime(created_time)
        created_time = time.strftime("%Y-%m-%d %H:%M:%S", created_time)
        print(f"Created Time: {created_time}")

        if current_time > created_time:
            td = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(created_time, "%Y-%m-%d %H:%M:%S")
            print(f"Time Difference: {td}")

        else:
            td = datetime.strptime(created_time, "%Y-%m-%d %H:%M:%S") - datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S")
            print(f"Time Difference: {td}")

        if td.total_seconds() < 1500:
            print("Time difference is less than 60 seconds, time difference is:", td)
            print("Sending Slack Message to Audit")

            post_slack(detail)

        else:
            print("Time difference is greater than 60 seconds, time difference is:", td)
            print("No new mail found")
    print("=====================================================")
if __name__ == "__main__":
    main()
