import random
import multiprocessing
import time

#####################################################################################################################
class Home:
    def __init__(self, id, production_rate, consumption_rate, trade_policy):
        self.id = id
        self.production_rate = production_rate
        self.consumption_rate = consumption_rate
        self.trade_policy = trade_policy
        self.surplus = 0
        self.shortage = 0

    def update_surplus_shortage(self):
        self.surplus = self.production_rate - self.consumption_rate
        self.shortage = self.consumption_rate - self.production_rate

    def trade_energy(self, market_price):
        if self.trade_policy == 'always_give':
            return self.surplus
        elif self.trade_policy == 'always_sell':
            return -self.shortage
        else:  # self.trade_policy == 'sell_if_no_takers':
            if self.surplus > 0:
                return self.surplus
            elif self.shortage > 0 and market_price < threshold:
                return -self.shortage
            else:
                return 0

def generate_homes(num_homes):
    homes = []
    for i in range(num_homes):
        production_rate = random.uniform(0, 10)
        consumption_rate = random.uniform(0, 10)
        trade_policy = random.choice(['always_give', 'always_sell', 'sell_if_no_takers'])
        homes.append(Home(i, production_rate, consumption_rate, trade_policy))
    return homes

###################################################################################################################
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
            
################################################################################################################
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


###########################################################################################################
class Weather(multiprocessing.Process):
    def __init__(self, temperature_q):
        multiprocessing.Process.__init__(self)
        self.temperature_q = temperature_q

    def run(self):
        while True:
            temperature = random.uniform(10, 20)
            self.temperature_q.put(temperature)
            time.sleep(1)

##################################################################################################


if __name__ == '__main__':
    ###
    home_process = Home()
    home_process.start()

    ###
    weather_process = Weather()
    weather_process.start()

    ###
    external_process = External()
    external_process.start()

    ###
    market_process = Market()
    market_process.start()

