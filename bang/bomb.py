import time
from threading import Thread
from auth import (USERS_TOKENS, BOT_TOKEN)


class BombCountdown(Thread):
    def __init__(self, slack_client, data):
        Thread.__init__(self)
        self.slack_client = slack_client
        self.data = data

    def delete_line(self, data):
        # Delete command
        self.slack_client.api_call("chat.delete",
            token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
            channel=data['channel'], ts=data['ts'], as_user=True)

    def react(self, data, emoji):
        return self.slack_client.api_call("reactions.add",
            token=BOT_TOKEN, as_user=False, name=emoji, icon_emoji=':slack-cli:',
            channel=data['channel'], timestamp=data['ts'])

    def run(self):
        time.sleep(17)
        self.react(self.data, 'three')
        time.sleep(1)
        self.react(self.data, 'two')
        time.sleep(1)
        self.react(self.data, 'one')
        time.sleep(1)
        self.react(self.data, 'fire')
        self.delete_line(self.data)
