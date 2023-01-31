import random
import multiprocessing
import time

class Market(multiprocessing.Process):
    def __init__(self, event_q, temperature_array, market_pipe):
        multiprocessing.Process.__init__(self)
        self.event_q = event_q
        self.temperature_array = temperature_array
        self.market_pipe = market_pipe
        self.energy_price = 0.145
        self.gamma = 0.99

    def run(self):
        while True:
            event, event_coef = self.market_pipe.recv()
            temperature = self.temperature_array[0]
            f_0 = 1/temperature
            u_0 = event_coef
            self.energy_price = self.gamma * self.energy_price + 0.001 * f_0 + 0.01 * u_0
            print("Energy Price: {}".format(self.energy_price))
            time.sleep(1)
            

if __name__ == '__main__':
    event_q = multiprocessing.Queue()
    temperature_array = multiprocessing.Array('f', [0])
    market_pipe_parent, market_pipe_child = multiprocessing.Pipe()
    market = Market(event_q, temperature_array, market_pipe_parent)
    market.start()
    weather_p = multiprocessing.Process(target=weather_process, args=(temperature_array,))
    weather_p.start()
    external = External(event_q, event_coef, market_pipe_child)
    external.start()
