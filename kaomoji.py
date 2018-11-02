# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import logging
from rtmbot.core import Plugin

from rsrc.kaomoji import KAOMOJIS

u"""Replace (custom) emoji with its kaomoji equivalent (👁 ͜ʖ👁)
"""

BOT_TOKEN = 'xxxx'
USERS_TOKENS = {
    'U3M46A86A': 'xoxp-xxxxx',
}


class KaomojiPlugin(Plugin):

    def process_message(self, data):
        logging.basicConfig(filename='rtmbotf.log',
                            format='%(asctime)s %(message)s')

        if data.get('text', '').startswith('!k '):
            # Delete command
            self.slack_client.api_call("chat.delete",
                token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
                channel=data['channel'], ts=data['ts'], as_user=True)
            # Replace command by sentence with kaomoji
            if data['text'][4:-1] in KAOMOJIS:
                self.slack_client.api_call("chat.postMessage",
                    token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
                    as_user=True, text=KAOMOJIS[data['text'][4:-1]], channel=data['channel'])
