import os
from datetime import datetime, timedelta, timezone
from flask import Flask, jsonify, request
from slackeventsapi import SlackEventAdapter
from slack import WebClient
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from sqlalchemy import create_engine

# import pandas as pd
# from json import dumps

JST = timezone(timedelta(hours=+9), 'JST')

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

cred_dict = {
    "type": "service_account",
    "project_id": os.environ['SHEET_PROJECT_ID'],
    "private_key_id": os.environ['SHEET_PRIVATE_KEY_ID'],
    "private_key": os.environ['SHEET_PRIVATE_KEY'].replace('\\n', '\n'),
    "client_email": os.environ['SHEET_CLIENT_EMAIL'],
    "client_id": os.environ['SHEET_CLIENT_ID'],
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.environ['SHEET_CLIENT_X509_CERT_URL']
}

credentials = ServiceAccountCredentials.from_json_keyfile_dict(cred_dict, scope)

gc = gspread.authorize(credentials)
spreadsheet_key = os.environ['SPREADSHEET_KEY']

SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])

db_url = os.environ.get('DATABASE_URL')
engine = create_engine(db_url)
table = 'tweets'

app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = request.get_json()
    # dumped = dumps(data)
    # print(dumped)
    # print(type(data))
    if data['type'] == 'url_verification':
        return jsonify({'challenge': data['challenge']}), 200
    else:
        return jsonify({'test': 'test'}), 200


@app.route('/test')
def hello():
    return 'Hello, World!\n'


slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)


# create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    channel = event_data["event"]["item"]["channel"]
    ts = event_data["event"]["item"]["ts"]
    print(type(ts))
    print(emoji)
    # print(event_data)
    # client.chat_postMessage(channel=channel, text=text)
    convs = client.conversations_replies(channel=channel, ts=ts)
    content = convs["messages"][0]["attachments"][0]
    print(content)
    # print(convs)
    link = content["title_link"]
    text = content["text"]
    dt = datetime.fromtimestamp(int(ts[:10]), JST)
    dt = f"{dt:%Y-%m-%d %H:%M:%S}"
    print(dt)

    engine.execute(f"insert into {table} values ('{dt}', '{url}', '{text}', '{emoji}');")
    wrksht = gc.open_by_key(spreadsheet_key).sheet1
    if emoji == '-1':
        add_list = [dt, link, text]
        print(add_list)
        wrksht.append_row(add_list)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
