# -*- coding: utf-8 -*-

from auth import (USERS_TOKENS, BOT_TOKEN)

SLACK_CLIENT = None  # set at bang plugin creation


def init_client(slack_client):
    """Setup global slack client.
    """
    global SLACK_CLIENT
    SLACK_CLIENT = slack_client


def post(data, text, user=None):
    args = {'token': BOT_TOKEN, 'as_user': True, 'text': text, 'channel': data['channel'],
        'icon_emoji': ':bang:'}
    if user:
        args['token'] = USERS_TOKENS.get(data['user'], BOT_TOKEN)
    data = SLACK_CLIENT.api_call("chat.postMessage", **args)

def delete_line(data):
    """Delete command
    """
    SLACK_CLIENT.api_call("chat.delete",
        token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
        channel=data['channel'], ts=data['ts'], as_user=True)

def channels_info(data, channel=None):
    """Get channel infos.
    """
    res = SLACK_CLIENT.api_call("channels.info",
        token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
        channel=channel or data['channel'])
    if not res['ok']:
        post(data, res['error'].replace('_', ' ').capitalize())
    return res

def react(data, emoji):
    """Add reaction.
    """
    return SLACK_CLIENT.api_call("reactions.add",
        token=BOT_TOKEN, as_user=False, name=emoji, icon_emoji=':slack-cli:',
        channel=data['channel'], timestamp=data['ts'])
