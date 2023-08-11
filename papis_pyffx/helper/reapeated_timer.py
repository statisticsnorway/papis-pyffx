from threading import Thread, Event

# Copied from threading.Timer and modified run function repeatedly
class RepeatedTimer(Thread):
    """Call a function *repeatadly* after a specified number of seconds:
    checks list for elements of worktime time longer than interval
            t = Timer(30.0, dictionary)
            t.start()
            t.cancel()     # stop the timer's action
    Modified from threading.Timer
    """

    def __init__(self, interval : int, func : callable):
        Thread.__init__(self)
        self.interval = interval
        self.function = func
        self.finished = Event()

    def stop(self):
        """Stop the timer if it hasn't finished yet."""
        self.finished.set()

    def run(self):
        while not self.finished.wait(self.interval):
            self.function()
