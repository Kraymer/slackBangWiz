import logging
import re
from rtmbot.core import Plugin

from memedict import search

from bang.auth import (USERS_TOKENS, BOT_TOKEN)
from bang.bomb import BombCountdown
from bang.slacker import (delete_line, react)

logging.basicConfig(filename='rtmbotf.log',
                    format='%(asctime)s %(message)s')

MEME_RE = re.compile(r'\".*?\"')
POLL_RE = re.compile(r"(.*?)((:\w+:\s?)+)")



class BangPlugin(Plugin):
    """Bang !shortcuts for slack.
    """

    def process_message(self, data):
        if 'text' in data:
            command = data['text'].split(' ')[0]
            if command == '!b':
                self._bomb(data)
            if command == '!k':
                self._kaomoji(data)
            elif command == '!kym':
                self._kym(data)
            elif command == '!h':
                self._help(data)
            elif command == '!m':
                self._memegen(data)
            elif command == '!p':
                self._poll(data)

    def strip_command(self, data):
        return ' '.join(data['text'].split(' ')[1:])


    # Commands below

    def _help(self, data):
        """`!h`\tshow this help message.
        """
        commands = [x for x in dir(self) if x.startswith('_') and not x.startswith('__')]
        usage = '\n'.join([getattr(self, cmd).__doc__.strip() for cmd in sorted(commands)])
        self.slack_client.api_call("chat.postMessage", icon_emoji=':bangbang:',
            token=BOT_TOKEN, as_user=False,
            username='Bang',
            text=usage,
            channel=data['user'])

    def _bomb(self, data):
        """`!b <text>`\tdestruct message after 20 seconds.
        """
        text = self.strip_command(data)
        delete_line(data)
        data = self.slack_client.api_call("chat.postMessage",
            token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
            as_user=True, text=':bomb: %s' % text, channel=data['channel'])
        data.update(data['message'])
        BombCountdown(self.slack_client, data).start()

    def _kaomoji(self, data):
        """`!k <emoji>`\treplace emoji with kaomoji.
        """
        from bang.rsrc.kaomoji import KAOMOJIS
        text = self.strip_command(data)[1:-1]
        if text in KAOMOJIS:
            delete_line(data)
            self.slack_client.api_call("chat.postMessage",
                token=USERS_TOKENS.get(data['user'], BOT_TOKEN),
                as_user=True, text=KAOMOJIS[text], channel=data['channel'])

    def _kym(self, data):
        """`!kym <memoji>`\tprint description of given emoji.
        """
        emoji = self.split_command(data)
        term = ' '.join(emoji.split('_'))
        description = search(term)
        self.slack_client.api_call("chat.postMessage", icon_emoji=':%s:' % emoji,
            token=BOT_TOKEN, as_user=False,
            username=description.split('.')[0],
            text='.'.join(description.split('.')[1:]),
            channel=data['user'])

    def _memegen(self, data):
        """`!m <meme_name or memoji> "<top text>" "<bottom text>"`\tgenerate a meme image
        """
        delete_line(data)
        meme_name = self.strip_command(data).split(' ')[0]
        if meme_name.startswith(':'):
            meme_name = meme_name[1:-1]
        texts = re.findall(MEME_RE, data['text'])
        texts = [x[1:-1].replace(' ', '_') for x in texts]
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
                self.react(data, emoji)
            self.react(data, 'end')
