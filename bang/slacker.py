# -*- coding: utf-8 -*-

from auth import (USERS_TOKENS, BOT_TOKEN)


def delete_line(slack_client, data):
    # Delete command
    slack_client.api_call("chat.delete",
        token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
        channel=data['channel'], ts=data['ts'], as_user=True)


def react(slack_client, data, emoji):
    return slack_client.api_call("reactions.add",
        token=BOT_TOKEN, as_user=False, name=emoji, icon_emoji=':slack-cli:',
        channel=data['channel'], timestamp=data['ts'])
