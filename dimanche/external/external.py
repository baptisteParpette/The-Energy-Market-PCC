import random
import multiprocessing
import time

class External(multiprocessing.Process):
    def __init__(self, event_q, event_coef):
        multiprocessing.Process.__init__(self)
        self.event_q = event_q
        self.event_coef = event_coef

    def run(self):
        while True:
            event = random.choice(['law', 'diplomatic', 'social', 'fuel'])
            event_coef = self.event_coef.get(event)
            self.event_q.put((event, event_coef))
            time.sleep(5)

if __name__ == '__main__':
    event_q = multiprocessing.Queue()
    event_coef = {
        'law': 0.01,
        'diplomatic': 0.02,
        'social': 0.03,
        'fuel': 0.04
    }
    external = External(event_q, event_coef)
    external.start()
    while True:
        event, event_coef = event_q.get()
        print("Event: {} with coef: {}".format(event, event_coef))
