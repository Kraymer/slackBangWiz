# -*- coding: utf-8 -*-

import time
from threading import Thread

from slacker import (react, delete_line)


class BombCountdown(Thread):
    def __init__(self, slack_client, data):
        Thread.__init__(self)
        self.slack_client = slack_client
        self.data = data

    def run(self):
        time.sleep(57)
        react(self.data, 'three')
        time.sleep(1)
        react(self.data, 'two')
        time.sleep(1)
        react(self.data, 'one')
        time.sleep(1)
        react(self.data, 'fire')
        delete_line(self.data)
