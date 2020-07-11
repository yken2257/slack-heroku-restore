import os
from flask import Flask, jsonify, request
from slackeventsapi import SlackEventAdapter
from slack import WebClient
#from json import dumps


SLACK_SIGNING_SECRET = os.environ["SLACK_SIGNING_SECRET"]
client = WebClient(token=os.environ['SLACK_BOT_TOKEN'])
app = Flask(__name__)


@app.route('/', methods=['POST'])
def main():
    data = request.get_json()
    #dumped = dumps(data)
    #print(dumped)
    #print(type(data))
    if data['type'] == 'url_verification':
        return jsonify({'challenge': data['challenge']}), 200
    else:
        return jsonify({'test':'test'}), 200

@app.route('/test')
def hello():
    return 'Hello, World!\n'

slack_events_adapter = SlackEventAdapter(SLACK_SIGNING_SECRET, "/slack/events", app)


# Create an event listener for "reaction_added" events and print the emoji name
@slack_events_adapter.on("reaction_added")
def reaction_added(event_data):
    emoji = event_data["event"]["reaction"]
    channel = event["item"]["channel"]
    text = ":%s:" % emoji
    print(emoji)
    client.chat_postMessage(channel=channel, text=text)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 3000)))
