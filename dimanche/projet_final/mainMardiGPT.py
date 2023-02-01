import random
import multiprocessing
import time
import math
from numpy import random
import os, signal

class Weather(multiprocessing.Process):
    def __init__(self,shared):
        super().__init__()
        self.shared=shared

    def run(self):
        t=0.0
        dt=1/6
        while True:
            rdm=(random.normal()*dt)
            temperature = round((-7.5*math.sin((math.pi*t/12)+math.pi/6)+10.5)+(rdm),2)
            t=t+dt
            self.shared[0] = temperature
            self.shared[1] = t
            time.sleep(0.5)

class Market(multiprocessing.Process):
    def __init__(self,shared):
        super().__init__()
        self.shared=shared

    def run(self):
        temp=shared_memory[1]
        while True:
            while temp!=shared_memory[1]:
                temp=shared_memory[1]
                print("La température exterieur est de ", shared_memory[0]," °C")
       
    def child_handler(self,signum, frame):
        print("Received signal", signum, "in child process")

class Child_Market(multiprocessing.Process):
    def __init__(self, parent_pid):
        super().__init__()
        self.parent_pid = parent_pid

    def run(self):
        signal.signal(signal.SIGUSR1, self.child_handler)
        print("Child process of Market with PID", os.getpid())
        while True:
            pass

if __name__ == '__main__':
    shared_memory = multiprocessing.Value('d', 0.0)
    shared_memory = multiprocessing.Array('d', range(2))

    Process_weather = Weather(shared_memory)
    Process_weather.start()

    Process_Market = Market(shared_memory)
    Process_Market.start()

    # Create child process of Market
    Process_Child_Market = Child_Market(Process_Market.pid)
    Process_Child_Market.start()

    # Send signal to child process of Market
    time.sleep(5)
    os.kill(Process_Market.pid, signal.SIGUSR1)

    Process_weather.join()
    Process_Market.join()
    Process_Child_Market.join()

