from multiprocessing import Process, Value
import time


class Weather:
    def __init__(self):
        self.temperature = Value('d', 0.0)
    def run(self):
        while True:
            time.sleep(3)
            self.temperature.value += 1

class Market:
    def __init__(self, temperature):
        self.temperature = temperature
    def run(self):
        while True:
            time.sleep(3)
            print("temperature: ", self.temperature.value)

if __name__ == '__main__':
    weather = Weather()
    market = Market(weather.temperature)
    weather_process = Process(target=weather.run)
    market_process = Process(target=market.run)
    weather_process.start()
    market_process.start()
