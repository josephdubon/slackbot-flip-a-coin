import os
import random

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

app = Flask(__name__)

# http://localhost:{port}/slack/events
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_EVENTS_TOKEN"), "/slack/events", app)
# This is how we will communicate with slack
slack_web_client = WebClient(token=os.environ.get("SLACKBOT_TOKEN"))

# Specific Slack structure to send message.
# - A "" (blank) text section written in markdown
MESSAGE_BLOCK = {
    "type": "section",
    "text": {
        "type": "mrkdwn",
        "text": "",
    }
}


# Create message function with decorator
@slack_events_adapter.on("message")
def message(payload):
    # Get all event data from payload
    event = payload.get("event", {})
    # Get all text sent
    text = event.get("text")

    if "flip a coin" in text.lower():
        #  Get channel_id, so we know where to send our message
        channel_id = event.get("channel")
        # Generate a random int
        rand_int = random.randint(0, 1)
        # 0 is heads
        if rand_int == 0:
            results = "Heads"
        # Anything NOT 0 is tails
        else:
            results = "Tails"

        # Send user a friendly message
        message = f"The result is {results}!"

        # Fill blank text in section from line 17
        MESSAGE_BLOCK["text"]["text"] = message
        # Define message to send - Slack sends messages in 'blocks'
        # - Wrap MESSAGE_BLOCK in a list for error-free multiple block architecture
        message_to_send = {
            "channel": channel_id,
            "blocks": [MESSAGE_BLOCK]
        }

        return slack_web_client.chat_postMessage(**message_to_send)


# The function returns the message we want to display in the user’s browser.
# - The default content type is HTML, so HTML in the string will be rendered
# - by the browser.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
