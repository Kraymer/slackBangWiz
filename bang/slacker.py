# -*- coding: utf-8 -*-

from auth import (USERS_TOKENS, BOT_TOKEN)

SLACK_CLIENT = None  # set at bang plugin creation


def init_client(slack_client):
    """Setup global slack client.
    """
    global SLACK_CLIENT
    SLACK_CLIENT = slack_client


def post(data, text, as_user=None, username=None, icon_emoji=None, private=False):
    """Post text. By default as 'Bangwiz' user, on same channel than command is emitted.
    """
    args = {'token': BOT_TOKEN, 'as_user': True, 'text': text, 'channel': data['channel'],
        'icon_emoji': ':bang:', username='BangWiz'}
    if as_user:
        args['token'] = USERS_TOKENS.get(data['user'], BOT_TOKEN)
    if username:
        args['username'] = username
    if icon_emoji:
        args['icon_emoji'] = icon_emoji
    if private:
        args['channel'] = data['user']
    return SLACK_CLIENT.api_call("chat.postMessage", **args)

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


def users_list():
    """Return a dict of all users mapping id to real name.
    """
    users = SLACK_CLIENT.api_call('users.list', token=BOT_TOKEN)['members']
    return {x['id']: x.get('real_name', x['name']) for x in users}
    

def channels_list():
    """Return a dict of all channels mapping id to name.
    """
    users = SLACK_CLIENT.api_call('channels.list', token=BOT_TOKEN)['channels']
    return {x['id']: x['name'] for x in users}
