import sys
import time

class Streamer:
    def __init__(self, delay=0.01):
        self.delay = delay

    def write(self, token):
        sys.stdout.write(token)
        sys.stdout.flush()
        time.sleep(self.delay)