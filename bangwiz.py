# -*- coding: utf-8 -*-

import logging
import random
import re
from rtmbot.core import Plugin

from memedict import search

from bang.auth import (USERS_TOKENS, BOT_TOKEN)
from bang.bomb import BombCountdown
from bang import slacker

logging.basicConfig(filename='rtmbotf.log',
                    format='%(asctime)s %(message)s')

MEME_RE = re.compile(r'\".*?\"')
POLL_RE = re.compile(r"(.*?)((:\w+:\s?)+)")


class BangPlugin(Plugin):
    """Bang !shortcuts for slack.
    """

    def __init__(self, name=None, slack_client=None, plugin_config=None):
        super(BangPlugin, self).__init__(name, slack_client, plugin_config)
        slacker.init_client(self.slack_client)

    def process_message(self, data):
        if 'text' in data:
            command = data['text'].split(' ')[0]
            if command[0] == '!' and len(command) == 2:
                slacker.delete_line(data)
                if command == '!b':
                    self._bomb(data)
                elif command == '!d':
                    self._describe(data)
                elif command == '!h':
                    self._help(data)
                elif command == '!i':
                    self._insult(data)
                elif command == '!k':
                    self._kaomoji(data)
                elif command == '!m':
                    self._memegen(data)
                elif command == '!p':
                    self._poll(data)
                elif command == '!r':
                    self._random(data)

    def strip_command(self, data):
        return ' '.join(data['text'].split(' ')[1:])

    # Commands below

    def _bomb(self, data):
        """`!b <text>`\tdestruct message after 1 minute.
        """
        text = self.strip_command(data)
        data = self.slack_client.api_call("chat.postMessage",
            token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
            as_user=True, text=':bomb: %s' % text, channel=data['channel'])
        data.update(data['message'])
        BombCountdown(self.slack_client, data).start()

    def _describe(self, data):
        """`!d <memoji>`\tprint description of given emoji.
        """
        emoji = self.split_command(data)
        term = ' '.join(emoji.split('_'))
        description = search(term)
        self.slack_client.api_call("chat.postMessage", icon_emoji=':%s:' % emoji,
            token=BOT_TOKEN, as_user=False,
            username=description.split('.')[0],
            text='.'.join(description.split('.')[1:]),
            channel=data['user'])

    def _help(self, data):
        """`!h`\tshow this help message.
        """
        commands = [x for x in dir(self) if x.startswith('_') and not x.startswith('__')]
        usage = '\n'.join([getattr(self, cmd).__doc__.strip() for cmd in sorted(commands)])
        self.slack_client.api_call("chat.postMessage", icon_emoji=':exclamation:',
            token=BOT_TOKEN, as_user=False,
            username='Bang',
            text=usage,
            channel=data['user'])

    def _kaomoji(self, data):
        """`!k <emoji>`\treplace emoji with kaomoji.
        """
        from bang.rsrc.kaomoji import KAOMOJIS
        text = self.strip_command(data)[1:-1]
        if text in KAOMOJIS:
            self.slack_client.api_call("chat.postMessage",
                token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
                as_user=True, text=KAOMOJIS[text], channel=data['channel'])

    def _insult(self, data):
        """`!i <@USER>`\tthrow a bunch of shakespearian poisonous words at your opponent face
        """
        from bang.rsrc.insult import INSULTS
        text = self.strip_command(data)
        self.slack_client.api_call("chat.postMessage",
            token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
            as_user=True, text=':shakespeare: %s _%s_' % (
                text, random.choice(INSULTS)),
            channel=data['channel'])

    def _memegen(self, data):
        """`!m <meme_name or memoji> "<top text>" "<bottom text>"`\tgenerate a meme image
        """
        meme_name = self.strip_command(data).split(' ')[0]
        if meme_name.startswith(':'):
            meme_name = meme_name[1:-1]
        texts = re.findall(MEME_RE, data['text'])
        texts = [x[1:-1].replace('_', '__').replace(' ', '_').replace('-', '--').replace(
            '?', '~q').replace('%', '~p').replace('?', '~q').replace('/', '~s').replace(
            '#', '~h') for x in texts]
        url = 'https://memegen.link/%s/%s/%s.jpg' % (meme_name, texts[0], texts[1])
        self.slack_client.api_call("chat.postMessage",
            token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
            as_user=True, text=':troll: %s' % url, channel=data['channel'])

    def _poll(self, data):
        """`!p <question> <emojis>`\tpost an emopoll as bot user hence enabling original poster to vote.
        """
        text = self.strip_command(data)
        match = re.match(POLL_RE, text)
        question = match.group(1)
        emojis = [x for x in match.group(2).split(':') if x]
        if question and len(emojis) > 1:
            data = self.slack_client.api_call("chat.postMessage",
                token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
                as_user=True, text=':question: %s' % question, channel=data['channel'])
            data.update(data['message'])
            for emoji in emojis:
                slacker.react(data, emoji)
            slacker.react(data, 'void')

    def _random(self, data):
        """`!r [#CHANNEL]`\tpick a random user in the channel.
        """
        channel = self.strip_command(data)
        res = slacker.channels_info(data, channel)
        slacker.post(data, 'Random #%s user: %s' % (channel, random.choice(res['channel']['members'])))
