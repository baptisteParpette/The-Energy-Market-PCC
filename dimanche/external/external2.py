import random
import multiprocessing
import time

class External(multiprocessing.Process):
    def __init__(self, event_q, event_coef, market_pipe):
        multiprocessing.Process.__init__(self)
        self.event_q = event_q
        self.event_coef = event_coef
        self.market_pipe = market_pipe

    def run(self):
        while True:
            event = random.choice(['law', 'diplomatic', 'social', 'fuel'])
            event_coef = self.event_coef.get(event)
            self.market_pipe.send((event, event_coef))
            time.sleep(5)

if __name__ == '__main__':
    event_q = multiprocessing.Queue()
    event_coef = {
        'law': 0.01,
        'diplomatic': 0.02,
        'social': 0.03,
        'fuel': 0.04
    }
    market_pipe_parent, market_pipe_child = multiprocessing.Pipe()
    external = External(event_q, event_coef, market_pipe_child)
    external.start()
    
    while True:
        event, event_coef = market_pipe_parent.recv()
        print("Event: {} with coef: {}".format(event, event_coef))
        # the market process takes corresponding action impacting energy price here.
