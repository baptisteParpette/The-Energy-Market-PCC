import random
import multiprocessing
import time

class Weather(multiprocessing.Process):
    def __init__(self, temperature_q):
        multiprocessing.Process.__init__(self)
        self.temperature_q = temperature_q

    def run(self):
        while True:
            temperature = random.uniform(10, 20)
            self.temperature_q.put(temperature)
            time.sleep(1)

if __name__ == '__main__':
    temperature_q = multiprocessing.Queue()
    weather = Weather(temperature_q)
    weather.start()
    while True:
        temperature = temperature_q.get()
        print("Temperature is: {}".format(temperature))
