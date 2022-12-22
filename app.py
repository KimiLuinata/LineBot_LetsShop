import os
import sys
import graphviz

from flask import Flask, jsonify, request, abort, send_file
from dotenv import load_dotenv
from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from fsm import TocMachine
from utils import *

load_dotenv()


machine = TocMachine(
    states=["init", "start", "addBudget", "addList", "delList", "delete","addPrice", "addUnit", 
            "confirm", "menu", "checkBudget", "goodBudget", "badBudget", "finalConfirm", "showList"],
    transitions=[
        {
            "trigger": "advance",
            "source": "init",
            "dest": "start",
            "conditions": "is_going_to_start",
        },
        {
            "trigger": "advance",
            "source": "start",
            "dest": "addBudget",
            "conditions": "is_going_to_addBudget",
        },
        {
            "trigger": "advance",
            "source": "addBudget",
            "dest": "addList",
            "conditions": "is_going_to_addList",
        },
        {
            "trigger": "advance",
            "source": "addBudget",
            "dest": "delList",
            "conditions": "is_going_to_delList",
        },
        {
            "trigger": "advance",
            "source": "delList",
            "dest": "delete",
            "conditions": "is_going_to_delete",
        },
        {
            "trigger": "advance",
            "source": "delete",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "addList",
            "dest": "addPrice",
            "conditions": "is_going_to_addPrice",
        },
        {
            "trigger": "advance",
            "source": "addPrice",
            "dest": "addUnit",
            "conditions": "is_going_to_addUnit",
        },
        {
            "trigger": "advance",
            "source": "addUnit",
            "dest": "confirm",
            "conditions": "is_going_to_confirm",
        },
        {
            "trigger": "advance",
            "source": "confirm",
            "dest": "addList",
            "conditions": "is_going_to_addListAgain",
        },
        {
            "trigger": "advance",
            "source": "confirm",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "checkBudget",
            "conditions": "is_going_to_checkBudget",
        },
        {
            "trigger": "advance",
            "source": "checkBudget",
            "dest": "goodBudget",
            "conditions": "is_going_to_goodBudget",
        },
        {
            "trigger": "advance",
            "source": "checkBudget",
            "dest": "badBudget",
            "conditions": "is_going_to_badBudget",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "addList",
            "conditions": "is_going_to_addList",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "delList",
            "conditions": "is_going_to_delList",
        },
        {
            "trigger": "advance",
            "source": "menu",
            "dest": "showList",
            "conditions": "is_going_to_showList",
        },
        {
            "trigger": "advance",
            "source": "goodBudget",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "showList",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "advance",
            "source": "goodBudget",
            "dest": "finalConfirm",
            "conditions": "is_going_to_finalConfirm",
        },
        {
            "trigger": "advance",
            "source": "badBudget",
            "dest": "menu",
            "conditions": "is_going_to_menu",
        },
        {
            "trigger": "go_back", 
            "source": ["init", "start", "addBudget", "addList", "delList", "delete","addPrice", "addUnit", 
                "confirm", "menu", "checkBudget", "goodBudget", "badBudget", "finalConfirm", "showList"], 
            "dest": "init"
        },

    ],
    initial="init",
    auto_transitions=False,
    show_conditions=True,
)

app = Flask(__name__, static_url_path="")


# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv("LINE_CHANNEL_SECRET", None)
channel_access_token = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", None)
if channel_secret is None:
    print("Specify LINE_CHANNEL_SECRET as environment variable.")
    sys.exit(1)
if channel_access_token is None:
    print("Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.")
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
parser = WebhookParser(channel_secret)


@app.route("/callback", methods=["POST"])
def callback():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue

        line_bot_api.reply_message(
            event.reply_token, TextSendMessage(text=event.message.text)
        )

    return "OK"


@app.route("/webhook", methods=["POST"])
def webhook_handler():
    signature = request.headers["X-Line-Signature"]
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info(f"Request body: {body}")

    # parse webhook body
    try:
        events = parser.parse(body, signature)
    except InvalidSignatureError:
        abort(400)

    # if event is MessageEvent and message is TextMessage, then echo text
    for event in events:
        if not isinstance(event, MessageEvent):
            continue
        if not isinstance(event.message, TextMessage):
            continue
        if not isinstance(event.message.text, str):
            continue
        print(f"\nFSM STATE: {machine.state}")
        print(f"REQUEST BODY: \n{body}")
        response = machine.advance(event)
        if response == False:
            # machine.get_graph().draw("fsm.png", prog="dot", format="png")
            if event.message.text.lower() == 'fsm':
                send_image_message(event.reply_token, 'https://mail.google.com/mail/u/2?ui=2&ik=918d7096bf&attid=0.1&permmsgid=msg-f:1752933235927965202&th=1853ab7d9a765e12&view=fimg&fur=ip&sz=s0-l75-ft&attbid=ANGjdJ-Z4CWLX8OfnT1Z2nZRRWFec-AIMTYUczltbVJ727Cq_AYPRWvWx0GKOjA7hqSBU4G7M1bzCElXLVc3peLiU39zWG5gL4WZEQ4d7ENesHo1P3mEiJVtKjIl8cU&disp=emb&realattid=ii_lbzbbq840')
            if machine.state != 'init' and event.message.text.lower() == 'restart':
                send_text_message(event.reply_token, "Hi! Let's plan your shopping list!\n"
                                            "Please enter \"start\"!")
                machine.go_back()
            else:	
                send_text_message(event.reply_token, "I don't understand, please re-type!")

    return "OK"


@app.route("/show-fsm", methods=["GET"])
def show_fsm():
    machine.get_graph().draw("fsm.png", prog="dot", format="png")
    return send_file("fsm.png", mimetype="image/png")


if __name__ == "__main__":
    port = os.environ.get("PORT", 8000)
    app.run(host="0.0.0.0", port=port, debug=True)
