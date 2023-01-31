import random
import multiprocessing
import time
import math
from numpy import random
import matplotlib.pyplot as plt

class Weather(multiprocessing.Process):
    def __init__(self,shared):
        super().__init__()
        self.shared=shared

    def run(self):
        t=0.0
        dt=1/6
        temp = []
        temp = []
        absx = []
        while True:
            rdm=(random.normal()*dt)
            temperature = round((-7.5*math.sin((math.pi*t/12)+math.pi/6)+10.5)+(rdm),2)
            t=t+dt
            temp += [temperature]
            self.shared.value = temperature
            print(self.shared.value)
            time.sleep(0.5)

        #plt.plot(absx,temp)
        #plt.show()

if __name__ == '__main__':
    #temperature_q = multiprocessing.Queue()
    #weather = Weather()
    #weather.start()
    #while i:
        #temperature = temperature_q.get()
        #print("Temperature is: {}".format(temperature))
    #data = Data()
    shared_memory = multiprocessing.Value('d', 0.0)

    child = Weather(shared_memory)
    child.start()
    temp=shared_memory.value
    while temp!=shared_memory.value:
        temp=shared_memory.value
        print("Data value after process execution:", shared_memory.value)

    child.join()
