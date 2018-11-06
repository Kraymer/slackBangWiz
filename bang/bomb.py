import time
from threading import Thread


class BombCountdown(Thread):
    def __init__(self, data):
        Thread.__init__(self)
        self.data = data

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
