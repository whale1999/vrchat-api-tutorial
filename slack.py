from urllib import request
import json
import requests

from config import SLACK_WEB_HOOK_URL


def send_slack_message(message):

    requests.post(SLACK_WEB_HOOK_URL, data=json.dumps({
    "text" : str(message),
    "icon_emoji" : ':robot:',
    "username" : 'My VRChat Develop Bot'
    }))