import random
import multiprocessing
import time

class Home(multiprocessing.Process):
    def __init__(self, home_pipe, temperature_array):
        multiprocessing.Process.__init__(self)
        self.home_pipe = home_pipe
        self.temperature_array = temperature_array
        
    def run(self):
        while True:
            temperature = self.temperature_array[0]
            self.home_pipe.send((temperature,))
            time.sleep(1)
            
class Weather(multiprocessing.Process):
    def __init__(self, temperature_array):
        multiprocessing.Process.__init__(self)
        self.temperature_array = temperature_array
        
    def run(self):
        while True:
            temperature = random.uniform(10, 20)
            self.temperature_array[0] = temperature
            time.sleep(1)

class External(multiprocessing.Process):
    def __init__(self, event_q, event_coef):
        multiprocessing.Process.__init__(self)
        self.event_q = event_q
        self.event_coef = event_coef
        
    def run(self):
        while True:
            event = random.choice(['law', 'diplomatic_tension', 'social_unrest', 'fuel_shortage'])
            event_coef = 0
            if event == 'law':
                event_coef = random.uniform(-0.05, 0.05)
            elif event == 'diplomatic_tension':
                event_coef = random.uniform(-0.1, 0.1)
            elif event == 'social_unrest':
                event_coef = random.uniform(-0.2, 0.2)
            elif event == 'fuel_shortage':
                event_coef = random.uniform(-0.3, 0.3)
            self.event_q.put((event, event_coef))
            time.sleep(1)

class Market(multiprocessing.Process):
    def __init__(self, home_pipe, event_q, temperature_array):
        multiprocessing.Process.__init__(self)
        self.home_pipe = home_pipe
        self.event_q = event_q
        self.temperature_array = temperature_array
        self.energy_price = 0.17

    def run(self):
        while True:
            temperature, = self.home_pipe.recv()
            event, event_coef = self.event_q.get()
            if temperature != 0:
                energy_price = (0.99 * self.energy_price) + (0.001 * (1/temperature)) + (event_coef)
            else:
                energy_price = (0.99 * self.energy_price) + (event_coef)
            self.energy_price = energy_price
            print(f'Energy price: {energy_price}')
            time.sleep(1)

if __name__ == '__main__':
    home_pipe, home_pipe_other = multiprocessing.Pipe()
    event_q = multiprocessing.Queue()
    temperature_array = multiprocessing.Array('f', [0])
    ###
    home_process = Home(home_pipe, temperature_array)
    home_process.start()

    ###
    weather_process = Weather(temperature_array)
    weather_process.start()

    ###
    event_coef = 0.01
    external_process = External(event_q, event_coef)
    external_process.start()

    ###
    market_process = Market(home_pipe_other, event_q, temperature_array)
    market_process.start()


